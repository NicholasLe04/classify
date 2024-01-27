from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

@app.get("/")
async def root():
    return { "message": "greetings traveller" }

if __name__ == "__main__":
    uvicorn.run("main:app")