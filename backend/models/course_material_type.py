from enum import Enum

class CourseMaterialType(Enum):
    SLIDES = "slides" # PDF presentation slides
    NOTES = "notes" # a PDF with written text e.g. the RL book from GenAI
    EXAM = "exam" # an exam