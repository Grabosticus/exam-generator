from pymongo import MongoClient
import os
import hashlib
from models.course_material_type import CourseMaterialType

# upload material -> check if material has already been uploaded via hashing it and looking into our mongo hash db
# if already uploaded, don't do anything
# also don't allow user to upload generated exams. Store the hash of generated exams in a db too and check
class HashDB:
    def __init__(self, mongo_url: str | None = None, client: MongoClient | None = None):
        mongo_url = mongo_url or os.environ.get("MONGO_URL", "mongodb://localhost:27017")
        self.client = client or MongoClient(mongo_url)
        self.db = self.client["hash_db"]
        self.collection = self.db["hashes"]

    def add_file_hash(self, course_id: int, hash: str, type: CourseMaterialType = None, generated: bool = False, filename: str = None):
        if generated:
            insert_type = "generated"
        else:
            insert_type = type.value
        hash_entry = {"course_id": course_id, "hash": hash, "type": insert_type}
        if filename:
            hash_entry["filename"] = filename
        self.collection.insert_one(hash_entry)

    def get_materials_for_course(self, course_id: int) -> list[dict]:
        """Returns list of materials (filename, type) for a course, excluding generated exams."""
        materials = self.collection.find(
            {"course_id": course_id, "type": {"$ne": "generated"}},
            {"_id": 0, "filename": 1, "type": 1}
        )
        return [m for m in materials if m.get("filename")]

    # returns {course_id, hash, type} or None if the hash doesn't exist yet for this course
    def get_file_hash(self, course_id: int, hash: str):
        file_hash = self.collection.find_one({"course_id": course_id, "hash": hash})
        return file_hash

    # we call this function for the uploaded files, since they might be 50MB large, therefore doing the hash in chunks seems better
    async def compute_file_hash(self, file):
        hasher = hashlib.sha256()

        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)

        await file.seek(0)
        file_sha256 = hasher.hexdigest()
        return file_sha256
    
    # we call this function for generated exams, since I asssume they won't be that large
    def compute_bytes_hash(self, bytes):
        bytes_sha256 = hashlib.sha256(bytes).hexdigest()
        return bytes_sha256
