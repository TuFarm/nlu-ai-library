# AI Agent Brief

## Scope completed

This repository is intentionally a scaffold, not a feature implementation. It establishes monorepo boundaries, runtime configuration, database model placeholders, API routing modules, service placeholders, and kiosk/web component entry points.

## Architecture map

- `backend/app/main.py`: FastAPI application factory, `/health`, and `/api/v1` router.
- `backend/app/core/`: environment-backed settings and SQLAlchemy engine/session/base.
- `backend/app/models/`: SQLAlchemy 2.x placeholders for `User`, `Book`, `BorrowingRecord`, `UserInteraction`, and `Recommendation`. `User.face_id_data` is JSON and must be revisited for biometric encryption, consent, retention, and deletion requirements before production.
- `backend/app/api/v1/routes/`: empty routers for users, books, borrowings, interactions, and recommendations.
- `backend/app/services/gemini_svc.py`: future Gemini NLP, mini-game generation, and recommendation integration boundary.
- `backend/app/services/library_svc.py`: future availability and borrowing transaction boundary.
- `backend/alembic/`: migration environment wired to all model metadata; no initial migration has been generated.
- `frontend/src/routes/`: route registry for registration and kiosk touchpoints.
- `frontend/src/components/`: minimal renderable placeholders for RemoteRegistrationForm, KioskHome, FaceIDScanner, and AIInteractionHub.
- `frontend/src/styles/global.css`: touchscreen baseline with 48px controls and a larger 1024x768+ kiosk breakpoint.
- `docker-compose.yml`: PostgreSQL and Redis only, for local infrastructure.

## Deliberate non-implementation

No authentication, face capture/recognition, sensor integration, CRUD handlers, borrowing transactions, Gemini calls, Redis client, schemas, relationships, initial Alembic revision, tests, or production deployment configuration has been implemented. Route and service modules are extension points.

## Recommended next steps

1. Confirm privacy and security requirements for biometric data before defining FaceID storage or capture behavior.
2. Add Pydantic schemas and explicit SQLAlchemy relationships and constraints.
3. Generate and review the initial Alembic migration against PostgreSQL.
4. Implement services first, then thin API endpoints, then frontend data clients.
5. Add backend/frontend tests and CI before integrating kiosk hardware or Gemini.

## Local commands

- Infrastructure: `docker compose up -d`
- Backend (from `backend`): `uvicorn app.main:app --reload`
- Migration generation (from `backend`): `alembic revision --autogenerate -m "initial schema"`
- Frontend (from `frontend`): `npm install`, then `npm run dev`

