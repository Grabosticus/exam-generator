import chromadb
from models.course_material_chunk import CourseMaterialChunk
from models.exam_question_chunk import ExamQuestionChunk
from models.course_material import CourseMaterial
from models.question import Question

"""
This class handles all interaction with our vector database.
"""
class VectorDB:

    # build your constructor here
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/chroma")
        self.course_material_collection = self.client.get_or_create_collection(
            name="course_material",
            metadata={"hnsw:space": "cosine"}
        )

        self.old_exam_collection = self.client.get_or_create_collection(
            name="old_exam_collection",
            metadata={"hnsw:space": "cosine"}
        )

    
    """
    Embeds a list of text with some embedding model.

    Input:
        texts... N texts
    Output:
        list[list[float]]... a list of N vector embeddings corresponding to the texts
    """
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        pass


    """
    Stores the course material in the `course_material_collection` in the Vector DB

    Input:
        chunks... Chunks of course material along with some metadata
    """
    def index_course_material(self, chunks: list[CourseMaterialChunk]) -> None:
        pass


    """
    Stores the old exam questions in the `old_exam_collection` in the Vector DB

    Input:
        chunks... Chunks of old exams (questions) along with some metadata
    """
    def index_old_exam_questions(self, chunks: list[ExamQuestionChunk]) -> None:
        pass

    
    """
    Retrieves relevant course material from the `course_material_collection`

    Input:
        course_id... The ID of the course to which the retrieved course material should belong
        query (Optional)... A query to specify which topics the retrieved course material should cover (e.g. "PPO, GRPO, Transformers")
        n (Optional)... How many course material examples should be retrieved

    Output:
        A list of `CourseMaterial`
    """
    def retrieve_course_material(self, course_id: int, query: str = "syllabus for the exam", n: int = 10) -> list[CourseMaterial]:
        pass


    """
    Retrieves old exam questions from the `old_exam_collection`

    Input:
        course_id... The ID of the course to which the retrieved exam questions should belong
        query (Optional)... A query to specify which topics the retrieved exam questions should cover (e.g. "PPO, GRPO, Transformers")
        n (Optional)... How many old exam questions should be retrieved

    Output:
        A list of `Question`
    """
    def retrieve_old_exam_questions(self, course_id: int, query: str = "exam questions", n: int = 10) -> list[Question]:
        pass