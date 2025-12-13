from typing import BinaryIO
from models.course_material_type import CourseMaterialType
from models.exam_question_chunk import ExamQuestionChunk
from models.course_material_chunk import CourseMaterialChunk

"""
This class extracts text from PDFs and enriches it with metadata.
"""
class FileProcessor:

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
        --> Think of different metadata that you could extract from the course material
        --> Think of different metadata that you could extract from the exam questions
    
    Since the "text" property of `ExamQuestionChunk` contains both the questions as well as its answer keys
    for multiple/single-choice questions, find a way to seperate them. If you use an AI to extract the PDF text,
    just tell it to format the text such that the answer keys come after some seperator like "[ANSWER_KEYS]",
    and that the individual answer keys should have a seperator as well, such as "[SEP]"
       --> e.g. ExamQuestionChunk.text = "What is 1+1? [ANSWER_KEYS] A) 2 [SEP] B) 5 [SEP] C) 1"



    Input:
        pdf_file... The uploaded PDF file
        material_type... The type of the PDF file (Notes, Slides, Exam, ...)
        course_id... The ID of the course that the material belong to

    Output:
        A tuple with the following entries:
        list[dict]... A list of dictionaries, containing all the chunk metadata. (list[i] contains the chunk metadata for chunk i)
                      e.g. {'has_images': true, 'topic': 'grpo'}
        list[CourseMaterialChunk] or list[ExamQuestionChunk]... The PDF text as a list of chunks, depending on the `material_type`
    """
    def chunk_and_enrich(
        self, 
        pdf_file: BinaryIO, 
        material_type: CourseMaterialType, 
        course_id: int
    ) -> tuple[list[dict], list[CourseMaterialChunk] | list[ExamQuestionChunk]]:
        pass