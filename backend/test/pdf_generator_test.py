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
            answer_keys=["Python", "HTML", "Car", "Java", "Something", "C#"]
        ),

        Question(
            question="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
            question_type=QuestionType.TEXT_ANSWER,
            metadata={"topic": "miscellaneous"}
        ),

        Question(
            question="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
            question_type=QuestionType.MULTIPLE_CHOICE,
            metadata={"topic": "miscellaneous"},
            answer_keys=["Mmm yes", "rather no", "what even is this question", "this is a very long answer option so that I can test how the text wraps inside the table, I hope it looks nice, but even if it is not especially nice I hope it is at least decent, I am slowly running out of random stuff to write but hopefully this is already at least three lines"]
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