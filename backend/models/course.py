from dataclasses import dataclass
from pydantic import BaseModel

"""
This class represents a course.
"""
@dataclass
class Course:
    course_id: int
    name: str

"""
This class is used to return courses to the frontend.
"""
class CourseModel(BaseModel):
    course_id: int
    name: str


class CourseCreateDTO(BaseModel):
    name: str