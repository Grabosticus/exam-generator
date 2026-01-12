from models.question import Question
from models.question_type import QuestionType

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


"""
This is the service that converts the LLM responses into an exam PDF.
"""
class PDFGenerator:

    # build your constructor here
    def __init__(self):
        self.page_size = A4
        self.margin_x = 50
        self.margin_y = 800
        self.line_height = 18


    """
    Takes the given questions and generates a new exam PDF for the given course ID.
        --> Think of ways to generate PDFs that look different e.g. by using different PDF templates

    Input: 
        questions... A list of generated questions (see `Question`)
        course_id... The ID of the course for which the exam is generated

    Output: 
        bytes... A PDF that represents an exam for the course with all questions in it.
    """
    def generate_pdf(self, questions: list[Question], course_id: int) -> bytes:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=self.page_size)

        x = self.margin_x
        y = self.margin_y

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(x, y, f"Exam for Course ID: {course_id}")
        y -= 2 * self.line_height

        c.setFont("Helvetica", 12)

        for idx, question in enumerate(questions, start=1):
            # Add a new page if we run out of space
            if y < 100:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = self.margin_y

            # Draw question text
            c.drawString(x, y, f"{idx}. {question.question}")
            y -= self.line_height

            # Handle question types
            if question.question_type in (
                QuestionType.MULTIPLE_CHOICE,
                QuestionType.SINGLE_CHOICE
            ) and question.answer_keys:
                for option_idx, option in enumerate(question.answer_keys):
                    c.drawString(x + 20, y, f"{chr(65 + option_idx)}. {option}")
                    y -= self.line_height

            elif question.question_type == QuestionType.TEXT_ANSWER:
                # Leave space for written answers
                for _ in range(3):
                    c.drawString(x + 20, y, "_" * 80)
                    y -= self.line_height

            y -= self.line_height  # Extra spacing between questions

        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer.read()