from os import getenv

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader

from models.courses import CourseRequest, CourseResponse
from utils.data import find_related_courses, add_course_data

load_dotenv()

router = APIRouter()
api_key_header = APIKeyHeader(name="x-api-key")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == getenv("API_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )

@router.post("/get-courses/", response_model=CourseResponse)
async def get_courses(request_body: CourseRequest, api_key: str = Security(get_api_key)):
    courses = find_related_courses(
        request_body.user_query,
        request_body.limit
    )
    courses = add_course_data('./utils/descriptions.json', courses)
    return { "courses": courses }

