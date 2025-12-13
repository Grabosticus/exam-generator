import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.vector_db import VectorDB
from models.course_material_chunk import CourseMaterialChunk
from models.course_material import CourseMaterial
from models.exam_question_chunk import ExamQuestionChunk
from models.question import Question
from models.question_type import QuestionType

def test1_adding_and_retrieving_course_material_chunks_without_query():

    print(f"\nTEST 1: Adding and retrieving course material chunks without query\n")

    # Arrange
    vector_db = VectorDB(db_path="data/test")
    course_id = 567539432943783438

    chunk_1 = CourseMaterialChunk(
        id="1", 
        course_id=course_id, 
        chunk_ind=0, 
        text="This is a text about PPO, "
    )
    metadata_1 = {"topic": "PPO"}

    chunk_2 = CourseMaterialChunk(
        id="2",
        course_id=course_id,
        chunk_ind=1,
        text="which is a loss function to optimize"
    )
    metadata_2 = {"topic": "loss function"}

    chunk_3 = CourseMaterialChunk(
        id="3",
        course_id=course_id,
        chunk_ind=2,
        text=" LLMs via Reinforcement Learning"
    )
    metadata_3 = {"topic": "LLMs, Reinforcement Learning"}

    chunks = [chunk_1, chunk_2, chunk_3]
    metadatas = [metadata_1, metadata_2, metadata_3]

    # Act
    vector_db.index_course_material(chunks=chunks, metadata=metadatas)

    course_material: list[CourseMaterial] = vector_db.retrieve_course_material(
        course_id=course_id,
        query=None,
        n=2
    )

    # Assert
    assert len(course_material) == 2
    print("Retrieved the following course material: ")
    for i, course_material_entry in enumerate(course_material):
        print(f"\nMATERIAL {i}")
        print(f"TEXT: {course_material_entry.text}")
        print(f"METADATA: {course_material_entry.metadata}")

    vector_db.delete_course_data(course_id=course_id)
    vector_db.delete_collections()

    print(f"TEST 1 PASSED\n")


def test2_adding_and_retrieving_old_exam_questions_without_query():

    print(f"\nTEST 2: Adding and retrieving old exam questions without query\n")

    # Arrange
    vector_db = VectorDB(db_path="data/test")
    course_id = 567539432943783438

    chunk_1 = ExamQuestionChunk(
        id="1",
        course_id=course_id,
        chunk_ind=0,
        text="What is the use of PPO in LLMs? [ANSWER_KEYS] A) It is useless [SEP] B) It is a loss function [SEP] C) I am not sure (Half points)",
        question_type=QuestionType.SINGLE_CHOICE
    )
    metadata_1 = {"topic": "PPO"}

    chunk_2 = ExamQuestionChunk(
        id="2",
        course_id=course_id,
        chunk_ind=1,
        text="What are the benefits of using GRPO compared to PPO? [ANSWER_KEYS] A) It is simpler [SEP] B) It is better for reasoning [SEP] C) It is generally worse than PPO",
        question_type=QuestionType.MULTIPLE_CHOICE
    )
    metadata_2 = {"topic": "PPO, GRPO"}

    chunk_3 = ExamQuestionChunk(
        id="3",
        course_id=course_id,
        chunk_ind=2,
        text="Explain in a few sentences how Self-Attention works in Transformers!",
        question_type=QuestionType.TEXT_ANSWER
    )
    metadata_3 = {"topic": "transformers, self-attention"}

    chunks = [chunk_1, chunk_2, chunk_3]
    metadatas = [metadata_1, metadata_2, metadata_3]

    # Act
    vector_db.index_old_exam_questions(chunks=chunks, metadata=metadatas)

    questions: list[Question] = vector_db.retrieve_old_exam_questions(course_id=course_id, query=None, n=2)

    # Assert
    assert len(questions) == 2
    print("Retrieved the following old exam questions: ")
    for i, question_entry in enumerate(questions):
        print(f"\nQUESTION {i}")
        print(f"QUESTION: {question_entry.question}")
        print(f"QUESTION_TYPE: {question_entry.question_type}")
        print(f"ANSWER_KEYS: {question_entry.answer_keys}")
        print(f"METADATA: {question_entry.metadata}")

    vector_db.delete_course_data(course_id=course_id)
    vector_db.delete_collections()

    print(f"TEST 2 PASSED\n")

def test3_adding_and_retrieving_old_exam_questions_with_query():

    print(f"\nTEST 3: ADDING AND RETRIEVING OLD EXAM QUESTIONS WITH QUERY")

    # Arrange
    vector_db = VectorDB(db_path="data/test")
    course_id = 567539432943783438

    chunk_1 = ExamQuestionChunk(
        id="1",
        course_id=course_id,
        chunk_ind=0,
        text="What is the use of PPO in LLMs? [ANSWER_KEYS] A) It is useless [SEP] B) It is a loss function [SEP] C) I am not sure (Half points)",
        question_type=QuestionType.SINGLE_CHOICE
    )
    metadata_1 = {"topic": "PPO"}

    chunk_2 = ExamQuestionChunk(
        id="2",
        course_id=course_id,
        chunk_ind=1,
        text="What are the benefits of using GRPO compared to PPO? [ANSWER_KEYS] A) It is simpler [SEP] B) It is better for reasoning [SEP] C) It is generally worse than PPO",
        question_type=QuestionType.MULTIPLE_CHOICE
    )
    metadata_2 = {"topic": "PPO, GRPO"}

    chunk_3 = ExamQuestionChunk(
        id="3",
        course_id=course_id,
        chunk_ind=2,
        text="Explain in a few sentences how Self-Attention works in Transformers!",
        question_type=QuestionType.TEXT_ANSWER
    )
    metadata_3 = {"topic": "transformers, self-attention"}

    chunk_4 = ExamQuestionChunk(
        id="4",
        course_id=course_id,
        chunk_ind=3,
        text="Explain the Chinese Room Argument in two sentences",
        question_type=QuestionType.TEXT_ANSWER
    )
    metadata_4 = {"topic": "CHINA"}

    chunks = [chunk_1, chunk_2, chunk_3, chunk_4]
    metadatas = [metadata_1, metadata_2, metadata_3, metadata_4]

    # Act
    vector_db.index_old_exam_questions(chunks=chunks, metadata=metadatas)

    query = "Reinforcement Learning"
    questions: list[Question] = vector_db.retrieve_old_exam_questions(course_id=course_id, query=query, n=2)

    # Assert
    assert len(questions) == 2
    print("Retrieved the following old exam questions: ")
    for i, question_entry in enumerate(questions):
        print(f"\nQUESTION {i}")
        print(f"QUESTION: {question_entry.question}")
        print(f"QUESTION_TYPE: {question_entry.question_type}")
        print(f"ANSWER_KEYS: {question_entry.answer_keys}")
        print(f"METADATA: {question_entry.metadata}")

    vector_db.delete_course_data(course_id=course_id)
    vector_db.delete_collections()

    print(f"TEST 3 PASSED\n")

if __name__ == "__main__":
    test1_adding_and_retrieving_course_material_chunks_without_query()
    test2_adding_and_retrieving_old_exam_questions_without_query()
    test3_adding_and_retrieving_old_exam_questions_with_query()