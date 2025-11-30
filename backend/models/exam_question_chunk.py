from dataclasses import dataclass
from models.question_type import QuestionType

"""
This class represents a chunk from an exam (a question).
It contains the actual question along with its type
"""
@dataclass
class ExamQuestionChunk:
    id: str # just in general, an id for this object

    course_id: int # the id of the course

    chunk_ind: int # the index of this chunk in the file it was extracted from

    text: str # the text in the chunk (a question + answer keys, if it is a multiple choice question)

    question_type: QuestionType # the question type (e.g. Single Choice, Multiple Choice, Text Answer, ...)
