from os import getenv

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader

from models.courses import CourseRequest, CourseResponse
from utils.data import find_related_courses, add_course_data
from utils.cache import LRUCache

load_dotenv()

router = APIRouter()
api_key_header = APIKeyHeader(name="x-api-key")

lru_cache = LRUCache(capacity=50)

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == getenv("API_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )

@router.post("/get-courses/", response_model=CourseResponse)
async def get_courses(request_body: CourseRequest, api_key: str = Security(get_api_key)):
    try:
        cache_key = (
            request_body.school,
            request_body.user_query,
            request_body.limit
        )
        if LRUCache.contains(cache_key):
            return LRUCache.get(cache_key)
        else:
            courses = find_related_courses(
                request_body.school,
                request_body.user_query,
                request_body.limit
            )
            courses = add_course_data(request_body.school, courses)
            LRUCache.put(cache_key, courses)
            return { "courses": courses }
    except:
        return { "error": "error finding related courses" }

