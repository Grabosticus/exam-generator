from __future__ import annotations

import os
import re
import time
from typing import Any, BinaryIO, Iterable
from io import BytesIO
import logging

from pypdf import PdfReader

try:  # Optional OCR dependencies
    import pytesseract
    from PIL import Image, ImageOps, ImageFilter
except Exception:  # pragma: no cover - optional dependency
    pytesseract = None
    Image = None
    ImageOps = None
    ImageFilter = None

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover - optional dependency
    fitz = None

from models.course_material_type import CourseMaterialType
from models.exam_question_chunk import ExamQuestionChunk
from models.course_material_chunk import CourseMaterialChunk
from models.question_type import QuestionType

"""
This class extracts text from PDFs and enriches it with metadata.
"""
class FileProcessor:
    def __init__(
        self,
        text_chunk_size: int = 1200,
        text_chunk_overlap: int = 200,
        use_ocr: bool = True,
        max_images_per_page: int = 5,
        min_text_len_for_ocr: int = 50,
        ocr_max_dim: int = 2600,
        ocr_min_dim: int = 1200,
        ocr_psm: str = "3",
        ocr_log_text: bool = False,
        ocr_dpi: int = 300,
        ocr_lang: str = "eng+deu",
    ) -> None:
        """Configure chunk sizes.

        Args:
            text_chunk_size: Maximum characters per course-material chunk.
            text_chunk_overlap: Overlap between consecutive chunks to preserve context.
            use_ocr: Enable rendered-page OCR via PyMuPDF + Tesseract if available.
            max_images_per_page: Legacy cap for image-based OCR (kept for backward compatibility).
            min_text_len_for_ocr: If extracted text already meets this length, skip OCR to save time.
            ocr_max_dim: Resize images so longest edge is at most this many pixels (faster OCR).
            ocr_min_dim: If images are very small, upscale so the longest edge is at least this many pixels.
            ocr_psm: Tesseract page segmentation mode to use (string for pytesseract config).
            ocr_log_text: If True, log extracted OCR text per page (can be verbose).
            ocr_lang: Preferred Tesseract languages (comma/plus-separated, e.g., "eng", "deu", or "eng+deu").
        """
        if text_chunk_size <= 0:
            raise ValueError("text_chunk_size must be positive")
        if text_chunk_overlap < 0 or text_chunk_overlap >= text_chunk_size:
            raise ValueError("text_chunk_overlap must be non-negative and smaller than text_chunk_size")

        self.text_chunk_size = text_chunk_size
        self.text_chunk_overlap = text_chunk_overlap
        self.use_ocr = use_ocr and pytesseract is not None and Image is not None and fitz is not None
        self.max_images_per_page = max_images_per_page
        self.min_text_len_for_ocr = max(min_text_len_for_ocr, 0)
        self.ocr_max_dim = max(ocr_max_dim, 100)
        self.ocr_min_dim = max(ocr_min_dim, 32)
        self.ocr_psm = ocr_psm
        self.ocr_log_text = ocr_log_text
        self.ocr_dpi = max(72, ocr_dpi)
        self.ocr_lang = ocr_lang or "eng"
        self._ocr_checked = False
        self._logger = logging.getLogger(__name__)

    def _ensure_ocr_ready(self) -> bool:
        """Check that OCR dependencies and tesseract binary are available."""
        if self._ocr_checked:
            return self.use_ocr

        self._ocr_checked = True

        if not self.use_ocr:
            self._logger.info(
                "OCR disabled: use_ocr=%s pytesseract=%s PIL=%s fitz=%s",
                self.use_ocr,
                bool(pytesseract),
                bool(Image),
                bool(fitz),
            )
            return False

        try:
            version = pytesseract.get_tesseract_version()
            self._logger.info("Tesseract version detected: %s", version)
            try:
                langs = pytesseract.get_languages(config="")
                self._logger.info("Tesseract languages available: %s", langs)
                for required in ("eng", "deu"):
                    if required not in langs:
                        self._logger.warning("Tesseract language '%s' missing; OCR quality may suffer", required)
            except Exception:
                self._logger.debug("Could not list Tesseract languages", exc_info=True)
        except Exception:
            self._logger.exception("Tesseract executable not available; disabling OCR")
            self.use_ocr = False
            return False

        return True

    
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
        course_id: int,
    ) -> tuple[list[dict], list[CourseMaterialChunk] | list[ExamQuestionChunk]]:
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        reader = PdfReader(BytesIO(pdf_bytes))

        render_doc = None
        if self._ensure_ocr_ready():
            try:
                render_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            except Exception:
                self._logger.exception("Failed to open PDF with PyMuPDF; disabling OCR for this file")
                render_doc = None

        if len(reader.pages) == 0:
            raise ValueError("Provided PDF is empty or unreadable")

        self._logger.info(
            "Chunking start material_type=%s course_id=%s pages=%s use_ocr=%s max_images_per_page=%s",
            material_type,
            course_id,
            len(reader.pages),
            self.use_ocr,
            self.max_images_per_page,
        )
        start_time = time.time()

        try:
            if material_type == CourseMaterialType.EXAM:
                metadata, chunks = self._process_exam(reader, render_doc, course_id)
            elif material_type in (CourseMaterialType.SLIDES, CourseMaterialType.NOTES):
                metadata, chunks = self._process_course_material(reader, render_doc, course_id, material_type)

            else:
                raise ValueError(f"Unsupported material type: {material_type}")
        finally:
            if render_doc is not None:
                try:
                    render_doc.close()
                except Exception:
                    self._logger.debug("PyMuPDF document close failed", exc_info=True)

        self._logger.info(
            "Chunking complete material_type=%s course_id=%s chunks=%s duration=%.2fs",
            material_type,
            course_id,
            len(chunks),
            time.time() - start_time,
        )
        return metadata, chunks

    # ------------------------------------------------------------------
    # Internal helpers
    def _process_course_material(
        self,
        reader: PdfReader,
        render_doc: Any | None,
        course_id: int,
        material_type: CourseMaterialType,
    ) -> tuple[list[dict], list[CourseMaterialChunk]]:
        metadata: list[dict] = []
        chunks: list[CourseMaterialChunk] = []

        chunk_ind = 0
        for page_index, page in enumerate(reader.pages):
            page_start = time.time()
            text = page.extract_text() or ""
            ocr_text = ""
            ocr_lang_used: str | None = None
            has_images = self._page_has_images(page)
            self._logger.debug(
                "Page %s/%s materials has_images=%s initial_text_len=%s",
                page_index + 1,
                len(reader.pages),
                has_images,
                len(text),
            )
            run_ocr = render_doc is not None and self.use_ocr and self._needs_ocr(text)
            if not run_ocr:
                self._logger.debug(
                    "OCR skipped page %s native_len=%s threshold=%s",
                    page_index + 1,
                    len(text),
                    self.min_text_len_for_ocr,
                )
            if run_ocr:
                self._logger.debug("OCR: start page %s (materials)", page_index + 1)
                ocr_start = time.time()
                ocr_text, ocr_lang_used = self._extract_ocr_from_page(render_doc, page_index, native_text=text)
                self._logger.debug(
                    "OCR: end page %s (materials) ocr_chars=%s lang=%s duration=%.2fs",
                    page_index + 1,
                    len(ocr_text),
                    ocr_lang_used,
                    time.time() - ocr_start,
                )
                if self.ocr_log_text and ocr_text:
                    self._logger.info(
                        "OCR TEXT page %s (materials) chars=%s lang=%s\n%s",
                        page_index + 1,
                        len(ocr_text),
                        ocr_lang_used,
                        ocr_text,
                    )
                if ocr_text:
                    text = (text + "\n" + ocr_text).strip()
                else:
                    self._logger.debug("OCR: no text extracted on page %s", page_index + 1)

            for chunk_text in self._split_text(text, self.text_chunk_size, self.text_chunk_overlap):
                chunk_id = f"{course_id}-{material_type.value}-{chunk_ind}"
                chunks.append(
                    CourseMaterialChunk(
                        id=chunk_id,
                        course_id=course_id,
                        chunk_ind=chunk_ind,
                        text=chunk_text,
                    )
                )

                metadata.append(
                    {
                        "page_start": page_index + 1,
                        "page_end": page_index + 1,
                        "has_images": has_images,
                        "ocr_used": bool(ocr_text),
                        "ocr_language": ocr_lang_used or "",
                        "char_len": len(chunk_text),
                        "material_type": material_type.value,
                        "topic": "unknown",
                    }
                )
                chunk_ind += 1

            self._logger.debug(
                "Page %s/%s done chunks_on_page=%s duration=%.2fs",
                page_index + 1,
                len(reader.pages),
                chunk_ind,
                time.time() - page_start,
            )

        return metadata, chunks

    def _process_exam(
        self,
        reader: PdfReader,
        render_doc: Any | None,
        course_id: int,
    ) -> tuple[list[dict], list[ExamQuestionChunk]]:
        page_texts: list[str] = []
        page_ocr_flags: list[bool] = []
        page_ocr_langs: list[str | None] = []
        for page_index, page in enumerate(reader.pages):
            page_start = time.time()
            text = page.extract_text() or ""
            ocr_text = ""
            ocr_lang_used: str | None = None
            has_images = self._page_has_images(page)
            self._logger.debug(
                "Exam page %s/%s has_images=%s initial_text_len=%s",
                page_index + 1,
                len(reader.pages),
                has_images,
                len(text),
            )
            run_ocr = render_doc is not None and self.use_ocr and self._needs_ocr(text)
            if not run_ocr:
                self._logger.debug(
                    "OCR skipped exam page %s native_len=%s threshold=%s",
                    page_index + 1,
                    len(text),
                    self.min_text_len_for_ocr,
                )
            if run_ocr:
                self._logger.debug("OCR: start exam page %s", page_index + 1)
                ocr_start = time.time()
                ocr_text, ocr_lang_used = self._extract_ocr_from_page(render_doc, page_index, native_text=text)
                self._logger.debug(
                    "OCR: end exam page %s ocr_chars=%s lang=%s duration=%.2fs",
                    page_index + 1,
                    len(ocr_text),
                    ocr_lang_used,
                    time.time() - ocr_start,
                )
                if self.ocr_log_text and ocr_text:
                    self._logger.info(
                        "OCR TEXT page %s (exam) chars=%s lang=%s\n%s",
                        page_index + 1,
                        len(ocr_text),
                        ocr_lang_used,
                        ocr_text,
                    )
                if ocr_text:
                    text = (text + "\n" + ocr_text).strip()
                else:
                    self._logger.debug("OCR: exam page %s OCR returned empty", page_index + 1)
            page_texts.append(text)
            page_ocr_flags.append(bool(ocr_text))
            page_ocr_langs.append(ocr_lang_used)
            self._logger.debug(
                "Exam page %s/%s done duration=%.2fs",
                page_index + 1,
                len(reader.pages),
                time.time() - page_start,
            )

        full_text = "\n".join(page_texts)
        if not full_text.strip():
            raise ValueError("Exam PDF contains no extractable text")

        question_blocks = self._split_questions(full_text)
        metadata: list[dict] = []
        chunks: list[ExamQuestionChunk] = []

        for idx, block in enumerate(question_blocks):
            question_text, answer_keys = self._extract_question_and_answers(block)

            # Build chunk text respecting separator convention
            if answer_keys:
                answer_part = " [SEP] ".join(answer_keys)
                chunk_text = f"{question_text} [ANSWER_KEYS] {answer_part}"
            else:
                chunk_text = question_text

            question_type = self._infer_question_type(question_text, answer_keys)
            chunk_id = f"{course_id}-{CourseMaterialType.EXAM.value}-{idx}"

            chunks.append(
                ExamQuestionChunk(
                    id=chunk_id,
                    course_id=course_id,
                    chunk_ind=idx,
                    text=chunk_text,
                    question_type=question_type,
                )
            )

            metadata.append(
                {
                    "question_number": idx + 1,
                    "page_start": self._find_page_for_text(page_texts, block),
                    "page_end": self._find_page_for_text(page_texts, block),
                    "ocr_used": any(page_ocr_flags),
                    "has_choices": bool(answer_keys),
                    "char_len": len(chunk_text),
                    "question_type": question_type.value,
                    "topic": "unknown",
                    "difficulty": "unknown",
                    "ocr_languages_used": ",".join(lang for lang in page_ocr_langs if lang),
                }
            )

        return metadata, chunks

    def _split_text(self, text: str, chunk_size: int, overlap: int) -> Iterable[str]:
        text = text.strip()
        if not text:
            return []

        start = 0
        length = len(text)
        chunks: list[str] = []
        while start < length:
            end = min(length, start + chunk_size)
            chunks.append(text[start:end])
            if end == length:
                break
            start = max(end - overlap, end) if overlap >= chunk_size else end - overlap
        return chunks

    def _page_has_images(self, page) -> bool:
        try:
            resources = page.get("/Resources") or {}
            x_objects = resources.get("/XObject")
            if not x_objects:
                return False
            x_objects = x_objects.get_object()
            for obj in x_objects.values():
                obj_type = obj.get("/Subtype")
                if obj_type == "/Image":
                    return True
        except Exception:
            # Best-effort; if detection fails, assume no images
            return False
        return False

    def _needs_ocr(self, native_text: str) -> bool:
        text = (native_text or "").strip()
        if len(text) < self.min_text_len_for_ocr:
            return True
        return self._looks_like_garbage(text)

    def _looks_like_garbage(self, native_text: str) -> bool:
        """Return True if native_text is empty or mostly non-alphanumeric noise."""
        text = (native_text or "").strip()
        if not text:
            return True
        alnum = sum(ch.isalnum() for ch in text)
        ratio = alnum / max(len(text), 1)
        return ratio < 0.45

    def _extract_ocr_from_page(self, render_doc: Any, page_index: int, native_text: str = "") -> tuple[str, str | None]:
        """Render the full page to an image and run Tesseract OCR."""
        if not (pytesseract and Image and fitz):
            return "", None

        try:
            page = render_doc.load_page(page_index)
        except Exception:
            self._logger.exception("OCR: failed to load page %s for rendering", page_index + 1)
            return "", None

        try:
            zoom = self.ocr_dpi / 72.0
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        except Exception:
            self._logger.exception("OCR: failed to render page %s to image", page_index + 1)
            return "", None

        image, rotation = self._maybe_fix_rotation(image)
        use_preview = (not (native_text or "").strip()) or self._looks_like_garbage(native_text)
        lang = self._decide_ocr_language(native_text, image if use_preview else None)

        try:
            prepared = self._prepare_image_for_ocr(image)
            t0 = time.time()
            config = f"--oem 1 --psm {self.ocr_psm} -c preserve_interword_spaces=1 -c user_defined_dpi={self.ocr_dpi}"
            text = pytesseract.image_to_string(
                prepared,
                lang=lang,
                config=config,
            )
            duration = time.time() - t0
            self._logger.debug(
                "OCR: page %s rendered=%sx%s prep=%sx%s rot=%s lang=%s duration=%.2fs",
                page_index + 1,
                image.width,
                image.height,
                prepared.width,
                prepared.height,
                rotation,
                lang,
                duration,
            )
            return (text.strip() if text else "", lang)
        except Exception:
            self._logger.exception("OCR: tesseract failed on page %s", page_index + 1)
            return "", lang

    def _prepare_image_for_ocr(self, image):
        """Stronger preprocessing: grayscale, denoise, resize, binarize."""
        try:
            img = image.convert("L")
            if ImageOps:
                img = ImageOps.autocontrast(img)
            if ImageFilter:
                img = img.filter(ImageFilter.MedianFilter(size=3))

            long_edge = max(img.width, img.height)
            resample = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
            if long_edge < self.ocr_min_dim:
                scale = self.ocr_min_dim / float(long_edge)
                new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
                img = img.resize(new_size, resample=resample)
            elif long_edge > self.ocr_max_dim:
                scale = self.ocr_max_dim / float(long_edge)
                new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
                img = img.resize(new_size, resample=resample)

            threshold = self._otsu_threshold(img)
            binary = img.point(lambda p: 255 if p > threshold else 0, mode="1")
            return binary.convert("L")
        except Exception:
            self._logger.debug("OCR preprocessing failed; using original image", exc_info=True)
            return image.convert("L") if hasattr(image, "convert") else image

    def _maybe_fix_rotation(self, image):
        """Detect page orientation via OSD on a downscaled preview and rotate if needed."""
        if not pytesseract:
            return image, 0
        try:
            preview = image.copy()
            preview.thumbnail((1000, 1000))
            preview = preview.convert("L")
            osd = pytesseract.image_to_osd(preview, config="--psm 0")
            match = re.search(r"Rotate:\s*(\d+)", osd)
            if match:
                rotation = int(match.group(1)) % 360
                if rotation:
                    return image.rotate(-rotation, expand=True), rotation
        except Exception as e:
            # OSD often fails on pages with too few characters; this is expected
            self._logger.debug("OCR orientation detection skipped: %s", str(e).split('\n')[0])
        return image, 0

    def _decide_ocr_language(self, native_text: str, preview_image) -> str:
        # If caller explicitly requests combined languages, honor it.
        if "+" in (self.ocr_lang or ""):
            return self.ocr_lang

        text = native_text or ""
        if any(ch in text for ch in "äöüÄÖÜß"):
            return "deu"
        if text:
            return "eng"

        if preview_image is not None and pytesseract:
            try:
                preview = preview_image.copy()
                preview.thumbnail((800, 800))
                preview = preview.convert("L")
                preview_text = pytesseract.image_to_string(preview, lang="eng+deu", config="--oem 1 --psm 6")
                if any(ch in preview_text for ch in "äöüÄÖÜß"):
                    return "deu"
            except Exception:
                self._logger.debug("OCR preview language detection failed", exc_info=True)

        return self.ocr_lang or "eng"

    def _otsu_threshold(self, img) -> int:
        # img must be grayscale
        hist = img.histogram()
        total = sum(hist)
        sum_total = sum(i * hist[i] for i in range(256))
        sumB = 0
        wB = 0
        var_max = 0.0
        threshold = 0

        for t in range(256):
            wB += hist[t]
            if wB == 0:
                continue
            wF = total - wB
            if wF == 0:
                break
            sumB += t * hist[t]
            mB = sumB / wB
            mF = (sum_total - sumB) / wF
            var_between = wB * wF * (mB - mF) ** 2
            if var_between > var_max:
                var_max = var_between
                threshold = t
        return threshold

    def _split_questions(self, text: str) -> list[str]:
        pattern = re.compile(r"(?m)(?=^\s*\d+\s*[\.)]\s+)")
        matches = list(pattern.finditer(text))

        if not matches:
            return [text.strip()]

        blocks: list[str] = []
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[start:end].strip()
            if block:
                blocks.append(block)
        return blocks

    def _extract_question_and_answers(self, block: str) -> tuple[str, list[str] | None]:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            return "", None

        # Identify where answer options start (A), B), etc.)
        option_regex = re.compile(r"^[A-H][\).]\s+")
        split_idx = None
        for idx, line in enumerate(lines):
            if option_regex.match(line):
                split_idx = idx
                break

        if split_idx is None:
            # No explicit options found
            question_text = " ".join(lines)
            return question_text, None

        question_lines = lines[:split_idx]
        answer_lines = lines[split_idx:]

        question_text = " ".join(question_lines)
        answer_keys = answer_lines if answer_lines else None
        return question_text, answer_keys

    def _infer_question_type(self, question_text: str, answer_keys: list[str] | None) -> QuestionType:
        if not answer_keys:
            return QuestionType.TEXT_ANSWER

        hint_text = question_text.lower()
        multi_hints = ["select all", "choose all", "multiple", "two correct", "three correct"]
        if any(hint in hint_text for hint in multi_hints):
            return QuestionType.MULTIPLE_CHOICE

        # If more than one answer option we still consider single-choice unless hints say otherwise
        return QuestionType.SINGLE_CHOICE

    def _find_page_for_text(self, page_texts: list[str], snippet: str) -> int | None:
        """Heuristic: return the first page index (1-based) containing a substring of snippet."""
        snippet = (snippet or "").strip()
        if not snippet:
            return None
        preview = snippet[:200]
        for idx, text in enumerate(page_texts):
            if preview in text:
                return idx + 1
        return None