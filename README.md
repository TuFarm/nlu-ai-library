# AI-Integrated Library Management System

Monorepo foundation for a FastAPI backend and React/TypeScript web and touchscreen kiosk client.

## Local infrastructure

1. Copy `.env.example` to `.env` if you want to override defaults.
2. Run `docker compose up -d` to start PostgreSQL and Redis.
3. Install backend dependencies from `backend/requirements.txt`, then run `uvicorn app.main:app --reload` inside `backend`.
4. Run `npm install` and `npm run dev` inside `frontend`.

See `AGENT_BRIEF.md` before continuing implementation.

