# AI Agent Brief

## Scope after the 2026-09-02 redesign

This project is an **AI Library Receptionist / Kiosk Assistant**, not a Library Management System. The university already owns the system of record for catalog and circulation. Do not reintroduce full books/authors/publishers/copies/shelves/loans/returns, advanced recommendations, A/B infrastructure, warehouse dimensions/facts, or ML lineage unless the user explicitly expands scope.

The SQLAlchemy registry must contain exactly these 24 tables:

1. users
2. user_preferences
3. face_profiles
4. face_authentication_logs
5. devices
6. user_sessions
7. interaction_events
8. knowledge_sources
9. knowledge_documents
10. knowledge_chunks
11. conversations
12. conversation_messages
13. ai_requests
14. ai_responses
15. ai_feedback
16. prompt_versions
17. book_categories
18. suggested_books
19. book_suggestion_logs
20. surveys
21. survey_questions
22. survey_responses
23. survey_answers
24. daily_report_metrics

Last verification: 12 backend tests passed; PostgreSQL upgrade/downgrade SQL compiled; FastAPI imported; frontend production build passed. Live PostgreSQL migration was not run in the implementation environment.

## Architecture map

- `backend/app/models/schema.py`: all 24 typed SQLAlchemy models.
- `backend/app/models/__init__.py`: metadata registry; keep it complete and free of stale models.
- `backend/app/core/database.py`: engine/session, timestamp and soft-delete mixins.
- `backend/alembic/versions/20260902_0001_ai_kiosk_schema.py`: replacement initial migration; validates the exact table set.
- `backend/app/api/v1/router.py`: placeholder domain routers for users, FaceID, sessions, interactions, knowledge, conversations, AI, prompts, book suggestions, surveys, and reports.
- `backend/app/schemas/common.py`: minimal typed placeholder response.
- `backend/app/services/`: clear boundaries for face, knowledge parsing, RAG, AI, survey, reports, and user helpers.
- `backend/app/services/user_service.py`: `calculate_student_year`; do not persist derived student year.
- `frontend/src/components/`: kiosk and admin placeholder pages matching the simplified journey.
- `docs/database/`: authoritative scope/design/dictionary/ERD, AI-vs-reporting explanation, and redesign changelog.

## Intended product flow

Kiosk: home → create anonymous session → FaceID attempt → attach user on success or remain anonymous → conversation/message → retrieve active knowledge chunks → create AI request/response → optional simple book suggestion → optional feedback/survey → end session.

Admin: upload knowledge source → parse into document/chunks → view processing state → view basic daily report.

No real recognition, upload parsing, vector search, AI provider call, or CRUD is implemented yet. Placeholder routes/components must not be described as completed features.

## Data boundaries

AI response/improvement inputs: knowledge sources/documents/chunks, selected conversation messages, feedback, prompt versions, user preferences, identity-only face profiles, and simple suggested books.

Research/report inputs: sessions, interaction events, FaceID logs, AI requests/responses, suggestion logs, surveys/questions/responses/answers, and daily aggregates.

The AI does not retrain itself from database records. Stored data supports RAG, limited context/memory, prompt versioning, feedback and evaluation. Any future training requires explicit consent, anonymization and governance.

## Safety and integrity rules

- Never store raw face photos or biometric data directly on users.
- A face profile must use an encrypted template or secure external reference; encryption/key management belongs to the security service.
- `face_authentication_logs.user_id` and `user_sessions.user_id` remain nullable for unknown/anonymous visitors.
- Append-only logs do not receive `deleted_at`; mutable configuration/business rows may use soft deletion.
- Avoid cascade deletion of factual history.
- Use `suggested_books.external_book_id` to integrate with the existing library system; do not mirror its catalog/circulation domain.
- `student_year = current_year - admission_year + 1`; missing or future admission years return `None`.
- Conversation history is not automatically authoritative knowledge.
- `daily_report_metrics` is derived and never replaces raw records.
- Do not add embeddings/pgvector before the vector stack is selected.

## Local verification

From `backend`:

```bash
alembic upgrade head --sql
python -m pytest -q
uvicorn app.main:app --reload
```

From `frontend`:

```bash
npm install
npm run build
npm run dev
```

Before deployment, run the migration against a disposable PostgreSQL 16 database and test both upgrade and downgrade.

## Remaining TODOs

- Live PostgreSQL migration/integration tests
- Request/response schemas and CRUD/service transactions
- Authentication/authorization and admin access
- Consent, retention, encryption and key management
- Face capture, liveness and recognition
- Upload validation/storage and PDF/Word/Excel/image parsing
- Chunking, retrieval and optional vector search
- AI provider execution, grounded citations and redaction
- Suggestion and survey APIs
- Idempotent daily-report aggregation job
- Real kiosk/admin UI and API clients
- CI/CD, backup and production observability

## Required change discipline

Keep the schema practical for a student research project. Add new tables only when a concrete kiosk requirement cannot be represented by the 24-table design. Import every model, review migrations manually, run backend tests and frontend build, and update the dictionary/ERD/changelog whenever schema semantics change.
