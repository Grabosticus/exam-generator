import io
from pathlib import Path

import pytest
from fpdf import FPDF

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.file_processor import FileProcessor
from models.course_material_type import CourseMaterialType
from models.question_type import QuestionType


def _build_pdf(pages: list[str]) -> io.BytesIO:
    """Create an in-memory PDF with the provided page texts."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=12)

    for content in pages:
        pdf.add_page()
        pdf.multi_cell(0, 10, content)

    pdf_bytes = pdf.output(dest="S").encode("latin1")
    return io.BytesIO(pdf_bytes)


def test_course_material_chunking_and_metadata():
    text_page_1 = "This is page one with enough text to require chunking. " * 4
    text_page_2 = "Second page with a bit more content to ensure multiple chunks." * 2
    pdf_stream = _build_pdf([text_page_1, text_page_2])

    processor = FileProcessor(text_chunk_size=60, text_chunk_overlap=10)
    metadata, chunks = processor.chunk_and_enrich(
        pdf_file=pdf_stream,
        material_type=CourseMaterialType.NOTES,
        course_id=123,
    )

    assert len(chunks) == len(metadata) > 1
    assert chunks[0].id == f"123-{CourseMaterialType.NOTES.value}-0"
    assert metadata[0]["page_start"] == 1
    assert metadata[0]["page_end"] == 1
    assert metadata[0]["has_images"] is False
    assert metadata[0]["material_type"] == CourseMaterialType.NOTES.value

    # Overlap check: the last 10 characters of chunk 0 should match the first 10 of chunk 1
    if len(chunks) > 1:
        assert chunks[0].text[-10:] == chunks[1].text[:10]


def test_exam_question_parsing_and_types():
    exam_text = """1. What is 2+2?
A) 3
B) 4
C) 5

2. Select all prime numbers:
A) 2
B) 4
C) 5
D) 9
"""
    pdf_stream = _build_pdf([exam_text])

    processor = FileProcessor()
    metadata, chunks = processor.chunk_and_enrich(
        pdf_file=pdf_stream,
        material_type=CourseMaterialType.EXAM,
        course_id=99,
    )

    assert len(chunks) == 2
    assert len(metadata) == 2

    q1 = chunks[0]
    assert "[ANSWER_KEYS]" in q1.text and "[SEP]" in q1.text
    assert q1.question_type == QuestionType.SINGLE_CHOICE
    assert metadata[0]["question_number"] == 1
    assert metadata[0]["has_choices"] is True

    q2 = chunks[1]
    assert q2.question_type == QuestionType.MULTIPLE_CHOICE
    assert metadata[1]["question_number"] == 2
    assert metadata[1]["has_choices"] is True
    assert metadata[1]["question_type"] == QuestionType.MULTIPLE_CHOICE.value
