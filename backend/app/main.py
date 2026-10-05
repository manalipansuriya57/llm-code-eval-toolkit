"""FastAPI app: list tasks, run tests, save rubric reviews."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .db import init_db, insert_review, list_reviews
from .runner import run_code_against_tests
from .tasks import TASKS

app = FastAPI(title="LLM Code-Response Evaluation Toolkit", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    task_id: str
    code: str


class ReviewRequest(BaseModel):
    task_id: str
    reviewer: str = Field(default="manalipansuriya57", min_length=1)
    code: str
    tests_passed: int
    tests_total: int
    correctness: int = Field(ge=1, le=5)
    efficiency: int = Field(ge=1, le=5)
    explanation: int = Field(ge=1, le=5)
    justification: str = Field(min_length=10)


@app.on_event("startup")
async def startup() -> None:
    await init_db()


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/tasks")
async def get_tasks():
    return [
        {
            "id": t["id"],
            "title": t["title"],
            "language": t["language"],
            "prompt": t["prompt"],
            "starter": t["starter"],
            "sample_response": t["sample_response"],
            "test_count": len(t["tests"]),
        }
        for t in TASKS
    ]


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if not task:
        raise HTTPException(404, "Task not found")
    return {
        "id": task["id"],
        "title": task["title"],
        "language": task["language"],
        "prompt": task["prompt"],
        "starter": task["starter"],
        "sample_response": task["sample_response"],
        "test_count": len(task["tests"]),
    }


@app.post("/run")
async def run_tests(body: RunRequest):
    task = next((t for t in TASKS if t["id"] == body.task_id), None)
    if not task:
        raise HTTPException(404, "Task not found")
    result = run_code_against_tests(body.code, task["tests"])
    return result


@app.post("/reviews")
async def create_review(body: ReviewRequest):
    if not any(t["id"] == body.task_id for t in TASKS):
        raise HTTPException(404, "Task not found")
    review_id = await insert_review(body.model_dump())
    return {"id": review_id, "status": "saved"}


@app.get("/reviews")
async def get_reviews():
    return await list_reviews()
