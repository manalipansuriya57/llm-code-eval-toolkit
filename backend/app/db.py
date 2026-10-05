"""SQLite persistence for evaluation reviews."""

from __future__ import annotations

import json
from pathlib import Path

import aiosqlite

DB_PATH = Path(__file__).resolve().parent.parent / "eval_reviews.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    code TEXT NOT NULL,
    tests_passed INTEGER NOT NULL,
    tests_total INTEGER NOT NULL,
    correctness INTEGER NOT NULL,
    efficiency INTEGER NOT NULL,
    explanation INTEGER NOT NULL,
    justification TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(SCHEMA)
        await db.commit()


async def insert_review(payload: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO reviews (
                task_id, reviewer, code, tests_passed, tests_total,
                correctness, efficiency, explanation, justification
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["task_id"],
                payload["reviewer"],
                payload["code"],
                payload["tests_passed"],
                payload["tests_total"],
                payload["correctness"],
                payload["efficiency"],
                payload["explanation"],
                payload["justification"],
            ),
        )
        await db.commit()
        return cursor.lastrowid or 0


async def list_reviews(limit: int = 50) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM reviews ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


def dump_json(obj) -> str:
    return json.dumps(obj, default=str)
