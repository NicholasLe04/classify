from pydantic import BaseModel
from typing import List

class Course(BaseModel):
    course_code: str
    course_description: str
    catoid: int
    coid: int

class CourseRequest(BaseModel):
    school: str
    user_query: str
    limit: int

class CourseResponse(BaseModel):
    courses: List[Course]