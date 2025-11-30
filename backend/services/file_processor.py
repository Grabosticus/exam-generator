from typing import BinaryIO
from models.course_material_type import CourseMaterialType
from models.exam_question_chunk import ExamQuestionChunk
from models.course_material_chunk import CourseMaterialChunk

"""
This class extracts text from PDFs and enriches it with metadata.
"""
class FileProcessor:

    CHUNK_SIZE = 0
    OVERLAP_SIZE = 0

    # build your constructor here
    def __init__(self):
        pass

    
    """
    Extracts the text from the PDF file and returns it as chunks of text, enriched with some metadata.
    Depending on the `material_type` different chunking strategies should be used.
    It isn't that important what strategies you use for slides and notes,
    but for exam questions a chunk needs to contain the whole question (+ answer keys, if it is multiple/single choice)

    Depending on the `material_type` different metadata should be extracted
    Currently, no metadata is extracted for both the course material and exam questions.

    (Optional: Think of different metadata that you could extract from the course material)
    (Optional: Think of different metadata that you could extract from the exam questions)


    Input:
        pdf_file... The uploaded PDF file
        material_type... The type of the PDF file (Notes, Slides, Exam, ...)
        course_id... The ID of the course that the material belong to

    Output:
        A tuple with the following entries:
        list[dict]... A list of dictionaries, containing all the chunk metadata. (list[i] contains the chunk metadata for chunk i)
        list[CourseMaterialChunk] or list[ExamQuestionChunk]... The PDF text as a list of chunks
    """
    def chunk_and_enrich(
        self, 
        pdf_file: BinaryIO, 
        material_type: CourseMaterialType, 
        course_id: int
    ) -> tuple[list[dict], list[CourseMaterialChunk] | list[ExamQuestionChunk]]:
        pass