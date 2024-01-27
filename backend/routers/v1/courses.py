from os import getenv

from dotenv import load_dotenv
from fastapi import APIRouter, Request

from models.courses import CourseRequest, CourseResponse
from utils.data import find_related_courses, add_descriptions

router = APIRouter()

load_dotenv()

@router.post("/get-courses/", response_model=CourseResponse)
async def get_courses(request_body: CourseRequest, request: Request):
    if "api_key" not in request.headers or request.headers["api_key"] != getenv("API_KEY"):
        return { "status": "unauthorized"} 
    else:
        courses = find_related_courses(
            request_body.user_query,
            request_body.limit
        )
        courses = add_descriptions('./utils/descriptions.json', courses)
        return { "courses": courses }

