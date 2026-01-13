from fastapi import FastAPI, UploadFile, File, Response, Query, HTTPException, status
from fastapi.responses import JSONResponse
from typing import BinaryIO
import io
import os
import sys
import logging
from dataclasses import asdict
from fastapi.middleware.cors import CORSMiddleware
# Ensure local services/ and models/ are importable when running directly (uvicorn backend.main:app)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from services.file_processor import FileProcessor
from services.vector_db import VectorDB
from services.question_generator import QuestionGenerator
from services.pdf_generator import PDFGenerator
from services.course_service import CourseService
from services.hash_db import HashDB
from models.course_material_type import CourseMaterialType
from models.course_material_chunk import CourseMaterialChunk
from models.question import Question
from models.course import CourseModel, Course, CourseCreateDTO
from models.course_material import CourseMaterial
from models.exam_question_chunk import ExamQuestionChunk

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
# Ingestion controls
def _env_bool(name: str, default: bool = True) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}

OCR_ENABLED = _env_bool("OCR_ENABLED", True)
OCR_MAX_IMAGES_PER_PAGE = int(os.getenv("OCR_MAX_IMAGES_PER_PAGE", "10"))
OCR_MIN_TEXT_FOR_OCR = int(os.getenv("OCR_MIN_TEXT_FOR_OCR", "0"))
OCR_MAX_DIM = int(os.getenv("OCR_MAX_DIM", "2600"))
OCR_MIN_DIM = int(os.getenv("OCR_MIN_DIM", "1200"))
OCR_PSM = os.getenv("OCR_PSM", "3")
OCR_LOG_TEXT = _env_bool("OCR_LOG_TEXT", False)
OCR_LANG = os.getenv("OCR_LANG", "eng+deu")

# Quiet noisy third-party debug logs (PIL, pytesseract, httpx, openai) while keeping our debug output
for noisy_logger in [
    "PIL",
    "PIL.PngImagePlugin",
    "pytesseract",
    "httpx",
    "openai",
]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

################################## If you add parameters to your constructors, add them here as well
file_processor = FileProcessor(
    use_ocr=OCR_ENABLED,
    max_images_per_page=OCR_MAX_IMAGES_PER_PAGE,
    min_text_len_for_ocr=OCR_MIN_TEXT_FOR_OCR,
    ocr_max_dim=OCR_MAX_DIM,
    ocr_min_dim=OCR_MIN_DIM,
    ocr_psm=OCR_PSM,
    ocr_log_text=OCR_LOG_TEXT,
    ocr_lang=OCR_LANG,
)
vector_db = VectorDB()
question_generator = QuestionGenerator()
pdf_generator = PDFGenerator()
course_service = CourseService()
hash_db = HashDB()
################################## (Also initializing these services here is kind of dirty, but I didn't care)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Our Frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

# POST Endpoint: Creates a new course with `name`
@app.post("/courses", status_code=201)
async def createCourse(course_create: CourseCreateDTO):
    try:
        createdCourse = course_service.create_course(name=course_create.name)
        return createdCourse
    except ValueError as e:
        # duplicate name or other validation issue
        raise HTTPException(status_code=409, detail=str(e))

# GET Endpoint: Returns a list of all courses
@app.get("/courses", response_model=list[CourseModel])
async def getAllCourses():
    courses: list[Course] = course_service.get_course_list()
    return [CourseModel(**asdict(course)) for course in courses]

# GET Endpoint: Returns the course with `course_id`
@app.get("/courses/{course_id}", response_model=CourseModel)
async def getCourse(course_id: int):
    try:
        course = course_service.get_course(course_id=course_id)
        return CourseModel(**asdict(course))
    
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")

"""
POST Endpoint for saving new course material.

Input:
    course_id... The ID of the course that the uploaded course material belongs to
    material_type... The type of the uploaded material (e.g. slides, notes, exam)
    file... The uploaded PDF
"""
@app.post("/courses/{course_id}/upload/{material_type}", status_code=200)
async def uploadFile(course_id: int, material_type: CourseMaterialType, file: UploadFile = File(...)):
    file_hash = await hash_db.compute_file_hash(file)
    saved_file_hash = hash_db.get_file_hash(course_id=course_id, hash=file_hash)
    if saved_file_hash is not None:
        message = get_conflict_message(material_type=saved_file_hash["type"])
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": message})

    pdf_bytes = await file.read()
    pdf_stream: BinaryIO = io.BytesIO(pdf_bytes)

    try:
        logger.info(f"Upload start course_id=%s material_type=%s size=%s bytes", course_id, material_type, len(pdf_bytes))

        if material_type == CourseMaterialType.EXAM:
            # 1) Extract text, chunk it, and enrich it with exam question metadata
            exam_question_metadata, exam_question_chunks = file_processor.chunk_and_enrich(pdf_file=pdf_stream, material_type=material_type, course_id=course_id)

            # 2) Save Exam Chunks in Vector DB
            vector_db.index_old_exam_questions(exam_question_chunks, exam_question_metadata)
        else:
            # 1) Extract text, chunk it, and enrich it with course material metadata
            course_material_metadata, course_material_chunks = file_processor.chunk_and_enrich(pdf_file=pdf_stream, material_type=material_type, course_id=course_id)

            # 2) Save Course Material in Vector DB
            vector_db.index_course_material(course_material_chunks, course_material_metadata)

        logger.info("Upload complete course_id=%s material_type=%s chunks=%s", course_id, material_type, len(exam_question_chunks if material_type == CourseMaterialType.EXAM else course_material_chunks))
        hash_db.add_file_hash(course_id=course_id, hash=file_hash, type=material_type)

        return Response(status_code=200)

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")
    except Exception:
        logger.exception("Upload failed course_id=%s material_type=%s", course_id, material_type)
        raise HTTPException(status_code=500, detail=f"Failed to save {material_type} for course {course_id}")

"""
POST Endpoint for new exam generation.

Input:
    course_id... the ID of the course for which the new exam should be generated
    n_questions (Optional)... The number of questions the new test should have
    topics (Optional)... The topics the new exam should focus on (e.g. Reinforcement Learning, Transformers, ...)
"""
@app.post("/courses/{course_id}/generate", status_code=200)
async def generateExam(course_id: int, n_questions: int = Query(20, ge=1, le=40), topics: str | None = Query(None, min_length=3, max_length=50)):

    try:
        # 1) Query Vector DB for relevant course material and old exam questions
        relevant_course_material: list[CourseMaterial] = vector_db.retrieve_course_material(course_id=course_id, query=topics)
        old_exam_questions: list[Question] = vector_db.retrieve_old_exam_questions(course_id=course_id, query=topics)
        
        # 2) Query LLM for new exam questions
        course = course_service.get_course(course_id)
        new_questions: list[Question] = question_generator.generate_questions(
            course_id=course_id,
            relevant_course_material=relevant_course_material,
            old_questions=old_exam_questions,
            n_new_questions=n_questions,
            course_name=course.name
        )

        # 3) Generate a new exam PDF based on the generated questions
        new_exam_pdf: bytes = pdf_generator.generate_pdf(questions=new_questions, course_id=course_id)
        bytes_hash = hash_db.compute_bytes_hash(new_exam_pdf)
        hash_db.add_file_hash(course_id=course_id, hash=bytes_hash, generated=True)

        return Response(content=new_exam_pdf, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="new_exam_course_{course_id}.pdf"'})
    
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to generate new exam for course {course_id}")


"""
DEBUG Endpoint: Inspect stored course material for a course.
Returns raw text chunks and metadata to aid debugging ingestion/embedding.
"""
@app.get("/debug/courses/{course_id}/material")
async def debug_get_course_material(course_id: int, query: str | None = Query(None), n: int = Query(5, ge=1, le=50)):
    try:
        materials: list[CourseMaterial] = vector_db.retrieve_course_material(course_id=course_id, query=query, n=n)
        return [
            {
                "text": m.text,
                "metadata": m.metadata,
            }
            for m in materials
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve course material for course {course_id}: {e}")


"""
DEBUG Endpoint: Inspect stored old exam questions for a course.
Returns question text, type, answer keys, and metadata to aid debugging ingestion/embedding.
"""
@app.get("/debug/courses/{course_id}/exams")
async def debug_get_exam_questions(course_id: int, query: str | None = Query(None), n: int = Query(5, ge=1, le=50)):
    try:
        questions: list[Question] = vector_db.retrieve_old_exam_questions(course_id=course_id, query=query, n=n)
        return [
            {
                "question": q.question,
                "question_type": q.question_type.value,
                "answer_keys": q.answer_keys,
                "metadata": q.metadata,
            }
            for q in questions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve exam questions for course {course_id}: {e}")


"""
DEBUG Endpoint: Generate exam questions without PDF generation.
Returns generated questions as JSON to inspect quality before PDF implementation.
"""
@app.post("/debug/courses/{course_id}/generate")
async def debug_generate_exam(course_id: int, n_questions: int = Query(5, ge=1, le=40), topics: str | None = Query(None, min_length=3, max_length=50)):
    try:
        logger.info("Debug generate start course_id=%s n_questions=%s topics=%s", course_id, n_questions, topics)

        # 1) Query Vector DB for relevant course material and old exam questions
        relevant_course_material: list[CourseMaterial] = vector_db.retrieve_course_material(course_id=course_id, query=topics)
        old_exam_questions: list[Question] = vector_db.retrieve_old_exam_questions(course_id=course_id, query=topics)

        logger.info("Debug generate retrieved material=%s old_questions=%s", len(relevant_course_material), len(old_exam_questions))

        # 2) Query LLM for new exam questions
        course = course_service.get_course(course_id)
        new_questions: list[Question] = question_generator.generate_questions(
            course_id=course_id,
            relevant_course_material=relevant_course_material,
            old_questions=old_exam_questions,
            n_new_questions=n_questions,
            course_name=course.name
        )

        logger.info("Debug generate complete course_id=%s generated=%s", course_id, len(new_questions))

        # Return as JSON for inspection
        return {
            "course_id": course_id,
            "course_name": course.name,
            "topics": topics,
            "n_requested": n_questions,
            "n_generated": len(new_questions),
            "context": {
                "course_material_chunks": len(relevant_course_material),
                "old_exam_questions": len(old_exam_questions),
            },
            "questions": [
                {
                    "question": q.question,
                    "question_type": q.question_type.value,
                    "answer_keys": q.answer_keys,
                    "metadata": q.metadata,
                }
                for q in new_questions
            ],
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Debug generate failed course_id=%s", course_id)
        raise HTTPException(status_code=500, detail=f"Failed to generate exam for course {course_id}: {e}")
    
def get_conflict_message(material_type: str):
    match material_type:
        case "exam": message = "This past exam has already been uploaded"
        case "notes": message = "These notes have already been uploaded"
        case "slides": message = "These slides have already been uploaded"
        case "generated": message = "You can't upload generated exams"
        case _: message = "This course material has already been uploaded"

    return message
