# Backend development setup

Python 3.12 and PostgreSQL 16 are recommended.

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
alembic upgrade head
python scripts/seed_dev.py
uvicorn app.main:app --reload
```

FastAPI can start before opening a DB connection because SQLAlchemy connects lazily. Starting it does not create the PostgreSQL database or tables. Use `alembic upgrade head`, then call `GET /api/v1/health/db`. Create a missing database in DBeaver, with `createdb`, or through the configured Docker Compose PostgreSQL service.

Configuration lives in `backend/.env`; copy `.env.example`. `FACE_PROVIDER`, `VOICE_PROVIDER` and `AI_PROVIDER` default to `mock`. A missing `GEMINI_API_KEY` never prevents startup. Future Gemini credentials belong only in `.env`, never source control.

The frontend may appear fully usable while this backend records nothing because its Phase 2 fallback catches API errors and uses local mock data. Inspect the browser network panel and `/api/v1/health/db` before assuming writes occurred.

Tests:

```powershell
python -m pytest -q
```

Tests not requiring PostgreSQL validate providers and API contracts. Full persistence, seed idempotency and migration checks should also run against a disposable PostgreSQL database.
