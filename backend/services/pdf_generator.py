from models.question import Question

"""
This is the service that converts the LLM responses into an exam PDF.
"""
class PDFGenerator:

    # build your constructor here
    def __init__(self):
        pass


    """
    Takes the given questions and generates a new exam PDF for the given course ID.

    (Optional, but very good to have: Think of ways to generate PDFs that look different e.g. by using different PDF templates)

    Input: 
        questions... A list of generated questions (see `Question`)
        course_id... The ID of the course for which the exam is generated

    Output: 
        bytes... A PDF that represents an exam for the course with all questions in it.
    """
    def generate_pdf(self, questions: list[Question], course_id: int) -> bytes:
        pass