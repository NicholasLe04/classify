from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.v1 import courses

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router, prefix="/api/v1")