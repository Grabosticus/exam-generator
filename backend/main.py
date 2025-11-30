from fastapi import FastAPI, UploadFile, File, Response, Query, HTTPException
from typing import BinaryIO
import io
from dataclasses import asdict
from services.file_processor import FileProcessor
from services.vector_db import VectorDB
from services.question_generator import QuestionGenerator
from services.pdf_generator import PDFGenerator
from services.course_service import CourseService
from models.course_material_type import CourseMaterialType
from models.course_material_chunk import CourseMaterialChunk
from models.question import Question
from models.course import CourseModel, Course
from models.course_material import CourseMaterial
from models.exam_question_chunk import ExamQuestionChunk

################################## If you add parameters to your constructors, add them here as well
file_processor = FileProcessor()
vector_db = VectorDB()
question_generator = QuestionGenerator()
pdf_generator = PDFGenerator()
course_service = CourseService()
################################## (Also initializing these services here is kind of dirty, but I didn't care)

app = FastAPI()

# TODO:
# upload material -> check if material has already been uploaded via hashing it and looking into our mongo hash db
# if already uploaded, don't do anything
# also don't allow user to upload generated exams. Store the hash of generated exams in a db too and check

# POST Endpoint: Creates a new course with `name`
@app.post("/courses", status_code=201)
async def createCourse(name: str):
    course_service.create_course(name=name)
    return Response(status_code=201)

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
    pdf_bytes = await file.read()
    pdf_stream: BinaryIO = io.BytesIO(pdf_bytes)

    try:

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

        return Response(status_code=200)

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to save {material_type} for course {course_id}")

"""
POST Endpoint for new exam generation.

Input:
    course_id... the ID of the course for which the new exam should be generated
    n_questions (Optional)... The number of questions the new test should have
    topic (Optional)... The topic the new exam should focus on (e.g. Reinforcement Learning, Transformers, ...)
"""
@app.post("/courses/{course_id}/generate", status_code=200)
async def generateExam(course_id: int, n_questions: int = Query(20, ge=1, le=40), topic: str | None = Query(None)):

    try:
        # 1) Query Vector DB for relevant course material and old exam questions
        if topic is not None:
            relevant_course_material: list[CourseMaterial] = vector_db.retrieve_course_material(course_id=course_id, query=topic)
            old_exam_questions: list[Question] = vector_db.retrieve_old_exam_questions(course_id=course_id, query=topic)
        else:
            relevant_course_material: list[CourseMaterial] = vector_db.retrieve_course_material(course_id=course_id)
            old_exam_questions: list[Question] = vector_db.retrieve_old_exam_questions(course_id=course_id)
        
        # 2) Query LLM for new exam questions
        new_questions: list[Question] = question_generator.generate_questions(
            course_id=course_id, 
            relevant_course_material=relevant_course_material, 
            old_questions=old_exam_questions, 
            n_new_questions=n_questions
        )

        # 3) Generate a new exam PDF based on the generated questions
        new_exam_pdf: bytes = pdf_generator.generate_pdf(questions=new_questions, course_id=course_id)

        return Response(content=new_exam_pdf, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="new_exam_course_{course_id}.pdf"'})
    
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")
    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to generate new exam for course {course_id}")
