from enum import Enum

"""
This class represents the different question types we handle/generate.
Feel free to add new types.
"""
class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple-choice"
    SINGLE_CHOICE = "single-choice"
    TEXT_ANSWER = "text-answer"