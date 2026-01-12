"""
File for testing the PDF generator without using the LLM or the actual application, using sample Question objects
Not necessary for the application
"""

from models.question import Question
from models.question_type import QuestionType
from services.pdf_generator import PDFGenerator


def main():
    questions = [
        Question(
            question="What is 2 + 2?",
            question_type=QuestionType.SINGLE_CHOICE,
            metadata={"topic": "math"},
            answer_keys=["3", "4", "5", "6"]
        ),
        Question(
            question="Explain the concept of polymorphism in OOP.",
            question_type=QuestionType.TEXT_ANSWER,
            metadata={"topic": "software engineering"}
        ),
        Question(
            question="Which of the following are programming languages?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            metadata={"topic": "computer science"},
            answer_keys=["Python", "HTML", "Car", "Java"]
        ),
    ]

    generator = PDFGenerator()
    pdf_bytes = generator.generate_pdf(questions, course_id=101)

    # Write the PDF to disk
    with open("example_exam_test.pdf", "wb") as f:
        f.write(pdf_bytes)

    print("PDF generated: example_exam_test.pdf")


if __name__ == "__main__":
    main()