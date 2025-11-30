from models.course import Course
from pymongo import MongoClient

"""
This class handles all requests that are made regarding creating/returning courses.
"""
class CourseService:
    
    def __init__(self, mongo_url: str = "mongodb://localhost:27017"):
        self.client = MongoClient(mongo_url)
        self.db = self.client["course_db"]
        self.collection = self.db["courses"]

    # BEWARE: This method might lead to concurrency issues, if two people are inserting a new course simultaneously
    def _get_next_course_id(self) -> int:
        last_highest = self.collection.find_one(sort=[("course_id", -1)])
        return 1 if last_highest is None else int(last_highest["course_id"]) + 1

    # creates a new course with the specified name
    def create_course(self, name: str) -> None:
        course_id = self._get_next_course_id()
        course = {"course_id": course_id, "name": name}
        self.collection.insert_one(course)

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