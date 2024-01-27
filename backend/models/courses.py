from pydantic import BaseModel
from typing import List

class Course(BaseModel):
    course_code: str
    course_description: str

class CourseRequest(BaseModel):
    user_query: str
    limit: int

class CourseResponse(BaseModel):
    courses: List[Course]