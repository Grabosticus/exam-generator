from models.course import Course
from pymongo import MongoClient, errors
import os

"""
This class handles all requests that are made regarding creating/returning courses.
"""
class CourseService:
    
    def __init__(self, mongo_url: str | None = None, client: MongoClient | None = None):
        """Init service; allow injecting client (for tests) and env-configurable URL."""
        mongo_url = mongo_url or os.environ.get("MONGO_URL", "mongodb://localhost:27017")
        self.client = client or MongoClient(mongo_url)
        self.db = self.client["course_db"]
        self.collection = self.db["courses"]
        # Ensure unique index on course name to prevent duplicates
        try:
            self.collection.create_index("name", unique=True)
        except errors.PyMongoError:
            # best-effort; if index creation fails we still run but rely on manual check
            pass

    # BEWARE: This method might lead to concurrency issues, if two people are inserting a new course simultaneously
    def _get_next_course_id(self) -> int:
        last_highest = self.collection.find_one(sort=[("course_id", -1)])
        return 1 if last_highest is None else int(last_highest["course_id"]) + 1

    # creates a new course with the specified name
    def create_course(self, name: str) -> Course:
        existing = self.collection.find_one({"name": name})
        if existing:
            raise ValueError(f"Course with name '{name}' already exists")
        course_id = self._get_next_course_id()
        course = {"course_id": course_id, "name": name}
        try:
            self.collection.insert_one(course)
            return Course(course_id=course_id, name=course["name"])
        except errors.DuplicateKeyError:
            # Race condition fallback: surface as ValueError consistent with manual check
            raise ValueError(f"Course with name '{name}' already exists")

    # returns a list of all courses
    def get_course_list(self) -> list[Course]:
        courses: list[Course] = []
        for course in self.collection.find():
            courses.append(Course(course_id=course["course_id"], name=course["name"]))
        return courses

    # returns the course with course_id
    def get_course(self, course_id: int) -> Course:
        course = self.collection.find_one({"course_id": course_id})
        if course is None:
            raise ValueError(f"Course with id {course_id} not found")
        return Course(course_id=course_id, name=course["name"])