# LLM Code-Response Evaluation Toolkit

Internal-style tool to rate LLM coding answers on **correctness**, **efficiency**, and **explanation quality**. Runs candidate code against unit tests and stores reviewer scores with written justifications.

## Stack

- **Backend:** Python, FastAPI, SQLite
- **Frontend:** React (Vite)

## Run

```bash
# Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — API at http://localhost:8000/docs.

## Features

- Sample coding tasks with hidden test cases
- Sandboxed-ish Python execution (`exec` with timeout + restricted builtins for demos)
- Rubric scoring (1–5) per dimension + free-text justification
- Reviewer session history persisted in SQLite

Use Python 3.11+ (<3.14) for the backend venv.
