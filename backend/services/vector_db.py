import chromadb
import logging
import os
import time
from chromadb.utils import embedding_functions
from models.course_material_chunk import CourseMaterialChunk
from models.exam_question_chunk import ExamQuestionChunk
from models.course_material import CourseMaterial
from models.question import Question
from models.question_type import QuestionType
import random

"""
This class handles all interaction with our vector database.
"""
class VectorDB:

    # build your constructor here
    def __init__(self, db_path="data/chroma", embedding_function=None, require_api_key: bool = True):
        api_key = os.environ.get("LLM_API_KEY")
        self._logger = logging.getLogger(__name__)
        if embedding_function is None:
            if require_api_key and not api_key:
                raise ValueError("LLM_API_KEY environment variable is not set")
            embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_base="https://openrouter.ai/api/v1",
                api_key=api_key,
                model_name="text-embedding-3-small"
            )

        self.embedding_function = embedding_function

        self.client = chromadb.PersistentClient(path=db_path)
        self.course_material_collection = self.client.get_or_create_collection(
            name="course_material",
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.embedding_function
        )

        self.old_exam_collection = self.client.get_or_create_collection(
            name="old_exam_collection",
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.embedding_function
        )

    def clean_md(self, md: dict) -> dict:
        return {k: v for k, v in md.items() if v is not None}
    
    """
    Embeds a list of text with some embedding model.

    Input:
        texts... N texts
    Output:
        list[list[float]]... a list of N vector embeddings corresponding to the texts
    """
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self.embedding_function(texts)


    """
    Stores the course material in the `course_material_collection` in the Vector DB

    Input:
        chunks... Chunks of course material along with some metadata
        metadata... Metadata of the course material chunks e.g. [{'topic': 'grpo', 'has_images': true}, {'topic': 'ppo', 'has_images': false}, ...]
    """
    def index_course_material(self, chunks: list[CourseMaterialChunk], metadata: list[dict]) -> None:
        self._logger.info("Indexing course material chunks=%s", len(chunks))

        if len(metadata) != len(chunks):
            raise ValueError("Error! Metadata list is not as long as the chunks list")
        
        ids = []
        documents = []
        metadatas = []

        for chunk, metadata_entry in zip(chunks, metadata):
            metadata_entry = self.clean_md(metadata_entry)
            ids.append(chunk.id)
            documents.append(chunk.text)
            combined_metadata = {
                "course_id": str(chunk.course_id),
                "chunk_ind": chunk.chunk_ind,
                **metadata_entry
            }
            metadatas.append(combined_metadata)

        batch_size = 64
        start_time = time.time()
        for i in range(0, len(ids), batch_size):
            effective_batch_size = batch_size
            if len(ids) - i < batch_size:
                effective_batch_size = len(ids) - i
            
            batch_ids = ids[i:i + effective_batch_size]
            batch_documents = documents[i:i + effective_batch_size]
            batch_metadata = metadatas[i:i + effective_batch_size]

            batch_start = time.time()
            self.course_material_collection.add(
                ids=batch_ids,
                documents=batch_documents,
                metadatas=batch_metadata
            )
            self._logger.debug(
                "Indexed course material batch size=%s offset=%s duration=%.2fs",
                len(batch_ids),
                i,
                time.time() - batch_start,
            )
        
        self._logger.info("Indexed course material complete total=%s duration=%.2fs", len(ids), time.time() - start_time)


    """
    Stores the old exam questions in the `old_exam_collection` in the Vector DB

    Input:
        chunks... Chunks of old exams (questions) along with some metadata
        metadata... Metadata of the exam question chunks e.g. [{'topic': 'grpo'}, {'topic': 'transformers'}, ...]
    """
    def index_old_exam_questions(self, chunks: list[ExamQuestionChunk], metadata: list[dict]) -> None:
        self._logger.info("Indexing old exam questions chunks=%s", len(chunks))        

        if len(chunks) != len(metadata):
            raise ValueError("Error! Metadata list is not as long as the chunks list")
        
        ids = []
        documents = []
        metadatas = []
        
        for chunk, metadata_entry in zip(chunks, metadata):
            metadata_entry = self.clean_md(metadata_entry)
            ids.append(chunk.id)
            documents.append(chunk.text)
            combined_metadata = {
                "course_id": str(chunk.course_id),
                "chunk_ind": chunk.chunk_ind,
                "question_type": chunk.question_type.value,
                **metadata_entry
            }
            metadatas.append(combined_metadata)
        
        batch_size = 64
        start_time = time.time()
        for i in range(0, len(ids), batch_size):
            effective_batch_size = batch_size
            if len(ids) - i < batch_size:
                effective_batch_size = len(ids) - i

            batch_ids = ids[i:i + effective_batch_size]
            batch_documents = documents[i:i + effective_batch_size]
            batch_metadata = metadatas[i:i + effective_batch_size]
            
            batch_start = time.time()
            self.old_exam_collection.add(
                ids=batch_ids,
                documents=batch_documents,
                metadatas=batch_metadata
            )
            self._logger.debug(
                "Indexed old exam batch size=%s offset=%s duration=%.2fs",
                len(batch_ids),
                i,
                time.time() - batch_start,
            )

        self._logger.info("Indexed old exam questions complete total=%s duration=%.2fs", len(ids), time.time() - start_time)

    
    """
    Retrieves relevant course material from the `course_material_collection`

    Input:
        course_id... The ID of the course to which the retrieved course material should belong
        query (Optional)... A query to specify which topics the retrieved course material should cover (e.g. "PPO, GRPO, Transformers")
        n (Optional)... How many course material examples should be retrieved

    Output:
        A list of `CourseMaterial`
    """
    def retrieve_course_material(self, course_id: int, query: str | None = None, n: int = 15) -> list[CourseMaterial]:
        self._logger.info("Retrieving course material course_id=%s query=%s n=%s", course_id, query, n)

        filter = {"course_id": str(course_id)}
        pool_size = n * 10  # when we have no query, we sample n * 10 entries from the DB and then select random entries out of that

        # if there is no query we just return the top n results without any semantic search
        if query is None or query.strip() == "":
            results = self.course_material_collection.get(
                where=filter,
                limit=pool_size,
                offset=random.randrange(0, max(1, self.course_material_collection.count() - pool_size + 1)),
                include=["documents", "metadatas"]
            )

            course_materials = []
            if results["ids"]:
                idx = random.sample(range(len(results["ids"])), k=min(n, len(results["ids"])))
                random_results = {k: [results[k][i] for i in idx] for k in ("ids", "documents", "metadatas")}

                for i in range(len(random_results["ids"])):
                    course_materials.append(
                        CourseMaterial(text=random_results["documents"][i], metadata=random_results["metadatas"][i])
                    )
            
            self._logger.info("Retrieved course material course_id=%s count=%s", course_id, len(course_materials))
            return course_materials
        
        # when we have a query, we filter by it
        results = self.course_material_collection.query(
            query_texts=[query],
            n_results=n,
            where=filter,
            include=["documents", "metadatas", "distances"]
        )

        course_materials = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                metadata = results["metadatas"][0][i].copy()
                metadata["relevancy_score"] = 1 - results["distances"][0][i] # i included this, maybe it is useful for the LLM

                course_materials.append(
                    CourseMaterial(text=results["documents"][0][i], metadata=metadata)
                )
        
        self._logger.info("Retrieved course material course_id=%s count=%s query=%s", course_id, len(course_materials), query)
        return course_materials


    """
    Retrieves old exam questions from the `old_exam_collection`

    Input:
        course_id... The ID of the course to which the retrieved exam questions should belong
        query (Optional)... A query to specify which topics the retrieved exam questions should cover (e.g. "PPO, GRPO, Transformers")
        n (Optional)... How many old exam questions should be retrieved

    Output:
        A list of `Question`
    """
    def retrieve_old_exam_questions(self, course_id: int, query: str | None = None, n: int = 15) -> list[Question]:
        self._logger.info("Retrieving old exam questions course_id=%s query=%s n=%s", course_id, query, n)

        filter = {"course_id": str(course_id)}
        pool_size = n * 10  # when we have no query, we sample n * 10 entries from the DB and then select random entries out of that to improve lecture coverage

        # we just retrieve n old questions
        if query is None or query.strip() == "":
            results = self.old_exam_collection.get(
                where=filter,
                limit=pool_size,
                offset=random.randrange(0, max(1, self.course_material_collection.count() - pool_size + 1)),
                include=["documents", "metadatas"]
            )

            questions = []
            if results["ids"]:
                idx = random.sample(range(len(results["ids"])), k=min(n, len(results["ids"])))
                random_results = {k: [results[k][i] for i in idx] for k in ("ids", "documents", "metadatas")}

                for i in range(len(random_results["ids"])):
                    metadata = random_results["metadatas"][i].copy()

                    question_type = metadata.pop("question_type")
                    question_type = QuestionType(question_type)

                    question_and_answers = random_results["documents"][i].split("[ANSWER_KEYS]")
                    question = question_and_answers[0]
                    if len(question_and_answers) > 1:
                        answer_keys_str = question_and_answers[1].strip()
                        answer_keys = [key.strip() for key in answer_keys_str.split("[SEP]") if key.strip()]
                    else:
                        answer_keys = None

                    questions.append(
                        Question(question=question, question_type=question_type, metadata=metadata, answer_keys=answer_keys)
                    )
                
            self._logger.info("Retrieved old exam questions course_id=%s count=%s", course_id, len(questions))
            return questions
            
        # we filter by the query
        results = self.old_exam_collection.query(
            query_texts=[query],
            n_results=n,
            where=filter,
            include=["documents", "metadatas", "distances"]
        )

        questions = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                metadata = results["metadatas"][0][i].copy()
                metadata["relevancy_score"] = 1 - results["distances"][0][i]

                question_type = metadata.pop("question_type")
                question_type = QuestionType(question_type)

                question_and_answers = results["documents"][0][i].split("[ANSWER_KEYS]")
                question = question_and_answers[0]
                if len(question_and_answers) > 1:
                    answer_keys_str = question_and_answers[1].strip()
                    answer_keys = [key.strip() for key in answer_keys_str.split("[SEP]") if key.strip()]
                else:
                    answer_keys = None

                questions.append(
                    Question(question=question, question_type=question_type, metadata=metadata, answer_keys=answer_keys)
                )
        
        self._logger.info("Retrieved old exam questions course_id=%s count=%s query=%s", course_id, len(questions), query)
        return questions
    
    """
    Deletes the data associated with a specific course id.
    I used this only for testing
    """
    def delete_course_data(self, course_id: int) -> None:
        self._logger.info("Deleting all material for course_id %s", course_id)

        filter = {"course_id": str(course_id)}
        
        material_results = self.course_material_collection.get(
            where=filter,
            include=[]
        )
        if material_results['ids']:
            self.course_material_collection.delete(ids=material_results['ids'])
        
        exam_results = self.old_exam_collection.get(
            where=filter,
            include=[]
        )
        if exam_results['ids']:
            self.old_exam_collection.delete(ids=exam_results['ids'])
        
        self._logger.info("Deleted all material for course_id %s", course_id)


    """
    Deletes all collections.
    I also only used this for testing
    """
    def delete_collections(self):
        self._logger.info("Deleting all collections...")
        self.client.delete_collection("course_material")
        self.client.delete_collection("old_exam_collection")