from fastapi import APIRouter

from models.courses import CourseRequest, CourseResponse
from utils.data import find_related_courses, add_descriptions

router = APIRouter()

@router.post("/get-courses/", response_model=CourseResponse)
async def get_courses(request_body: CourseRequest):
    courses = find_related_courses(
        request_body.user_query,
        request_body.limit
    )
    courses = add_descriptions('./utils/descriptions.json', courses)
    return { "courses": courses }

