#TODO: maybe Latex formatting
#done TODO: show if single choice or multiple choice
#done TODO: constants for indentations, rn I hardcoded 20 two times
#done TODO: stuff as class variables, not returned from methods (style, doc, etc)

from models.question import Question
from models.question_type import QuestionType

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Flowable, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT

from io import BytesIO

import datetime

#Helper class to draw boxes for answer options in SC and MC
class ChoiceBox(Flowable):
    def __init__(self, line_height):
        super().__init__()
        self.size = line_height*0.7
        self.height = line_height

    def draw(self):
        self.canv.rect(0, (self.height-self.size)/2, self.size, self.size)

#Helper class to draw lines for text answers
class AnswerLine(Flowable):
    def __init__(self, generator, line_width):
        super().__init__()
        self.length = generator.page_width-2*generator.margin_x-generator.question_indent
        self.line_width = line_width
        self.question_indent = generator.question_indent
    
    def draw(self):
        self.canv.setLineWidth(self.line_width)
        self.canv.line(self.question_indent, 0, self.length, 0)


"""
This is the service that converts the LLM responses into an exam PDF.
"""
class PDFGenerator:

    def create_document_template(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=self.margin_x,
            leftMargin=self.margin_x,
            topMargin=self.margin_y,
            bottomMargin=self.margin_y,
        )

        title_style = ParagraphStyle(
            "TitleStyle",
            alignment=TA_CENTER,
            fontSize=18,
            fontName="Times-Bold",
        )

        timestamp_style = ParagraphStyle(
            "TimestampStyle",
            fontName="Times-Italic",
            fontSize=12,
            alignment=1
        )

        question_style = ParagraphStyle(
            "QuestionStyle",
            fontName="Times-Roman",
            fontSize=12,
            leading=18,
            firstLineIndent=self.question_indent*(-1),
            leftIndent=self.question_indent,
            alignment=TA_JUSTIFY
        )

        option_style = ParagraphStyle(
            "OptionStyle",
            leftIndent=0,
            fontName="Times-Roman",
            fontSize=12,
            leading=18,
            alignment=TA_JUSTIFY
        )

        set_styles = {"title_style": title_style, "question_style": question_style, "option_style": option_style, "timestamp_style": timestamp_style}
        return (doc, set_styles)

    # build your constructor here
    def __init__(self):
        self.page_width, self.page_height = A4
        self.margin_x = 50
        self.margin_y = 50
        self.line_height = 18
        self.question_indent = 20

    

    def create_option_row(self, generator, doc, styles, option):
        choice_box = ChoiceBox(generator.line_height)
        option_row = Table(
            [[
                choice_box,
                Paragraph(f"{option}", styles["option_style"]),
            ]],
            colWidths=[choice_box.size + generator.question_indent/2,
                       generator.page_width - 2*generator.margin_x - choice_box.size - generator.question_indent*3]
            
        )

        option_row.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                #("GRID", (0, 0), (-1, -1), 0.25, "red")
            ])
        )

        return option_row

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
        # Create fresh buffer and document for each PDF generation
        self.buffer = BytesIO()
        self.doc, self.styles = self.create_document_template()

        current_date_time = datetime.datetime.now()
        current_date_time_str = current_date_time.strftime("%B %d, %Y at %H:%M:%S")

        story = []

        # Title
        story.append(Paragraph(f"Exam for Course ID: {course_id}", self.styles["title_style"]))
        story.append(Spacer(1, self.line_height))

        # Timestamp
        story.append(
            Paragraph(f"Generated at: {current_date_time_str}", self.styles["timestamp_style"])
        )
        story.append(Spacer(1, self.line_height))


        for idx, question in enumerate(questions, start=1):

            # Space between questions
            story.append(Spacer(1, self.line_height*0.7))

            # Question text (auto-wrapped)
            if question.question_type == QuestionType.MULTIPLE_CHOICE:
                story.append(
                    Paragraph(f"<b>Q{idx}.</b> {question.question}  <i><b>(MC)</b></i>", self.styles["question_style"])
                )

            elif question.question_type == QuestionType.SINGLE_CHOICE:
                story.append(
                    Paragraph(f"<b>Q{idx}.</b> {question.question} <i><b>(SC)</b></i>", self.styles["question_style"])
                )
            
            else:
                story.append(
                    Paragraph(f"<b>Q{idx}.</b> {question.question}", self.styles["question_style"])
                )

            if question.question_type in (
                QuestionType.MULTIPLE_CHOICE,
                QuestionType.SINGLE_CHOICE
            ) and question.answer_keys:
                story.append(Spacer(1, self.line_height*0.7))
                for option_idx, option in enumerate(question.answer_keys):
                    if (option_idx != 0):
                        story.append(Spacer(1, self.line_height*0.4))
                    story.append(self.create_option_row(self, self.doc, self.styles, option))
                

            elif question.question_type == QuestionType.TEXT_ANSWER:
                answer_lines = []
                for _ in range(3):
                    answer_lines.append(Spacer(1, self.line_height*1.5))
                    answer_lines.append(AnswerLine(self, 0.5))
                
                story.append(KeepTogether(answer_lines))
                story.append(Spacer(1, self.line_height*0.3))
                    

        self.doc.build(story)
        return self.buffer.getvalue()
