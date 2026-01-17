import os
import json
import logging
from openai import OpenAI
from models.question import Question
from models.course_material import CourseMaterial
from models.question_type import QuestionType

logger = logging.getLogger(__name__)

"""
This class generates new exam questions by querying an LLM via OpenRouter.
OpenRouter provides access to various LLM providers (OpenAI, Anthropic, Meta, etc.)
through a unified API that is compatible with the OpenAI SDK.
"""


class QuestionGenerator:

    def __init__(self):
        api_key = os.environ.get("LLM_API_KEY")
        if not api_key:
            raise ValueError("LLM_API_KEY environment variable is not set")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        # Default to Claude Sonnet 4.5 for better RAG reasoning
        # See https://openrouter.ai/models for available models
        self.model = os.environ.get("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250514")

    def _build_prompt(
            self,
            course_id: int,
            relevant_course_material: list[CourseMaterial],
            old_questions: list[Question],
            n_new_questions: int,
            course_name: str | None = None
    ) -> str:
        """Builds the prompt for the LLM."""

        # Use course_name if available, otherwise fall back to course_id
        if course_name:
            course_identifier = f'"{course_name}"'
        else:
            course_identifier = f"(Course ID: {course_id})"

        # Format course material
        course_material_text = ""
        for i, material in enumerate(relevant_course_material, 1):
            course_material_text += f"\n--- Course Material {i} ---\n{material.text}\n"
            if material.metadata:
                course_material_text += f"Metadata: {material.metadata}\n"

        # Format old questions as examples
        old_questions_text = ""
        for i, q in enumerate(old_questions, 1):
            old_questions_text += f"\n--- Example Question {i} ---\n"
            old_questions_text += f"Type: {q.question_type.value}\n"
            old_questions_text += f"Question: {q.question}\n"
            if q.answer_keys:
                old_questions_text += f"Answer Options: {', '.join(q.answer_keys)}\n"
            if q.metadata:
                old_questions_text += f"Metadata: {q.metadata}\n"

        prompt = f"""You are a professor teaching the TU Wien course {course_identifier}. Your task is to create a new exam for this course.

Your task is to generate {n_new_questions} new exam questions based on the provided course material.The new questions should be similar in style and difficulty to the example questions provided.

=== COURSE MATERIAL ===
{course_material_text if course_material_text else "No course material provided."}

=== EXAMPLE QUESTIONS FROM OLD EXAMS ===
{old_questions_text if old_questions_text else "No example questions provided."}

=== INSTRUCTIONS ===
1. Generate exactly {n_new_questions} new questions
2. Use a mix of question types: multiple-choice, single-choice, and text-answer
3. Questions should cover the topics from the course material
4. Match the style and difficulty of the example questions. Your generated questions should ideally be indistinguishable from the style of questions given in the example questions.
5. For multiple-choice and single-choice questions, provide 4 answer options
6. Ensure every question is clear and self-contained. If a question refers to a function, include the full function definition (or the relevant code snippet) directly in the question.
7. Use the same language as the course material and example questions (German or English).
8. Generate NEW questions - do not copy or closely paraphrase the example questions.

=== OUTPUT FORMAT ===
Return a valid JSON array with the following structure for each question:
[
  {{
    "question": "The question text",
    "question_type": "multiple-choice" | "single-choice" | "text-answer",
    "answer_keys": ["Option A", "Option B", "Option C", "Option D"] or null for text-answer,
    "metadata": {{"topic": "topic name", "difficulty": "easy|medium|hard"}}
  }}
]

IMPORTANT: Return ONLY the JSON array, no additional text or markdown formatting."""

        return prompt

    def _parse_response(self, response_text: str) -> list[Question]:
        """Parses the LLM response into Question objects."""

        # Clean potential markdown formatting
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            questions_data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response was: {response_text[:500]}...")
            raise ValueError(f"LLM response is not valid JSON: {e}")

        questions = []
        for q_data in questions_data:
            # Map question type string to enum
            q_type_str = q_data.get("question_type", "text-answer")
            try:
                q_type = QuestionType(q_type_str)
            except ValueError:
                logger.warning(f"Unknown question type '{q_type_str}', defaulting to TEXT_ANSWER")
                q_type = QuestionType.TEXT_ANSWER

            question = Question(
                question=q_data.get("question", ""),
                question_type=q_type,
                metadata=q_data.get("metadata", {}),
                answer_keys=q_data.get("answer_keys")
            )
            questions.append(question)

        return questions

    def generate_questions(
            self,
            course_id: int,
            relevant_course_material: list[CourseMaterial],
            old_questions: list[Question],
            n_new_questions: int = 20,
            course_name: str | None = None
    ) -> list[Question]:
        """
        Queries the LLM using a prompt enriched with relevant course material and old exam questions.

        Input:
            course_id... The ID of the course the exam questions should be generated for
            relevant_course_material... Relevant course material along with some metadata, queried from our vector DB
            old_questions... Old exam questions along with some metadata, queried from our vector DB
            n_new_questions... How many questions should be generated by the LLM
            course_name (Optional)... The name of the course (e.g. "Visual Computing"). If provided, used in prompt instead of course_id.

        Output:
            list[Question]... A list of N newly generated exam questions
        """

        prompt = self._build_prompt(
            course_id=course_id,
            relevant_course_material=relevant_course_material,
            old_questions=old_questions,
            n_new_questions=n_new_questions,
            course_name=course_name
        )

        log_identifier = course_name if course_name else f"course {course_id}"
        logger.info(f"Generating {n_new_questions} questions for {log_identifier} using model {self.model}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert exam question generator. You always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )

            response_text = response.choices[0].message.content
            logger.debug(f"LLM response received: {len(response_text)} characters")

            questions = self._parse_response(response_text)
            logger.info(f"Successfully generated {len(questions)} questions")

            return questions

        except Exception as e:
            logger.error(f"Error calling LLM API: {e}")
            raise
