# AI Agent Brief

## Current state

This repository is no longer only a database-model scaffold. It contains a production/research SQLAlchemy schema and an additive analytics/BI architecture, while the API, services, AI integrations, and UI remain mostly extension points.

The registered SQLAlchemy metadata currently contains:

- 92 tables
- 140 foreign keys
- 104 indexes
- Operational, research, telemetry, dashboard, staff/RBAC, academic, geographic, and ML-lineage domains

The last verified model suite reported `7 passed`. PostgreSQL upgrade and downgrade SQL generation also passed. A live PostgreSQL migration was not executed in the implementation environment because Docker was unavailable there.

## Repository map

- `backend/app/main.py`: FastAPI application factory, `/health`, and `/api/v1` router registration.
- `backend/app/core/config.py`: environment-backed application, PostgreSQL, Redis, and Gemini settings.
- `backend/app/core/database.py`: SQLAlchemy engine/session, declarative base, timestamp mixin, and soft-delete mixin.
- `backend/app/models/enums.py`: typed controlled vocabularies.
- `backend/app/models/schema.py`: operational and scientific-research models.
- `backend/app/models/analytics.py`: analytics dimensions/facts, AI/prompt registries, staff/RBAC, academic/geographic data, KPI/alerts, dashboards, and ML metadata.
- `backend/app/models/__init__.py`: mandatory metadata registry; Alembic depends on all models being imported here.
- `backend/app/api/v1/routes/`: currently empty routers for users, books, borrowing, interactions, and recommendations.
- `backend/app/services/`: placeholder Gemini and library-service boundaries.
- `backend/alembic/versions/20260829_0001_complete_schema.py`: initial operational/research schema.
- `backend/alembic/versions/20260829_0002_analytics_architecture.py`: additive analytics upgrade and AI registry references.
- `backend/tests/test_database_models.py`: structural mapper, DDL, relationship, constraint, grain, and cascade tests.
- `frontend/src/`: minimal React/TypeScript routes and kiosk-oriented components.
- `frontend/electron/`: Electron kiosk wrapper.
- `docs/database/`: database design, ERD, data dictionary, and definitions/calculations for 40 research metrics.
- `docs/dashboard/`: dashboard architecture, governed KPIs, future warehouse/star schema, and materialized-view recommendations.
- `docker-compose.yml`: PostgreSQL 16 and Redis 7 local infrastructure.

## Database architecture

### Operational and research domains

- Identity, preferences, consent history, data-subject requests, and anonymized research profiles
- Face profiles represented by encrypted templates or external secure references—never raw face images on `users`
- Devices, sessions, authentication attempts, and append-only interaction events
- Normalized books, authors, genres, publishers, copies, shelves, locations, and ebooks
- Search queries/results, AI requests/content, RAG documents/chunks/retrievals, and recommendations
- Games, borrowing/return attribution, notifications/reminders, and versioned surveys
- Research studies, anonymous participants, experimental groups, and time-bounded assignments
- Application performance/error telemetry and append-only security audit logs

### Analytics and dashboard domains

- `dim_date` and `dim_time` for calendar, fiscal, academic, holiday, and hourly analysis
- Eight daily aggregate facts: library usage, borrowing, search, recommendations, AI, games, authentication, and surveys
- AI model and prompt registries; legacy AI request text columns remain for backward compatibility
- Staff, departments, roles, permissions, assignments, and staff activities
- Faculties, majors, courses, academic profiles, and enrollments
- Reading rooms and time/location traffic snapshots
- Book popularity snapshots
- Governed dashboard metrics, alert rules/history, dashboards/widgets/layouts/filters/preferences
- ML datasets/versions, experiments, feature sets, training runs, and evaluation metrics

Daily fact tables supplement operational facts and must never become the source of transactional truth. Behavioral analysis should use immutable events; dashboard aggregates should be refreshed idempotently with `source_watermark` and `refreshed_at`.

## Important modeling rules

1. Preserve UUID primary keys, timezone-aware timestamps, explicit FKs, and current table names.
2. Treat `interaction_events`, `audit_logs`, and factual telemetry as append-only.
3. Do not cascade-delete research, audit, authentication, AI, recommendation, or borrowing history.
4. Use soft deletion only for mutable business/configuration entities.
5. Keep demographics separate from operational users and use anonymous participant codes for research exports.
6. Do not store raw biometric images, plaintext passwords, or unredacted sensitive AI content by default.
7. `RecommendationItem` and `SearchResult` convenience state does not replace timestamped interaction events.
8. Borrowing attribution should use `source_search_id` or `source_recommendation_item_id`, not redundant booleans.
9. Dashboard fact grain must be explicit and protected by unique constraints.
10. Large ML datasets, embeddings, and model artifacts belong in governed external storage; PostgreSQL stores references and lineage.

## Migration guidance

Run Alembic from `backend`:

```bash
alembic upgrade head
alembic current
```

The initial revision imports registered metadata rather than containing a fully frozen list of explicit operations. Revision `0002` therefore performs online schema inspection and is idempotent for both:

- an existing database created by the original `0001`; and
- a fresh database where live metadata makes `0001` see the current model registry.

Do not copy this pattern into future migrations. New revisions should use reviewed explicit Alembic operations and must not modify already-deployed historical revisions. Always test fresh upgrade, upgrade from the previous revision, and downgrade against PostgreSQL.

## Local setup and verification

Detailed Vietnamese instructions are in `README.md`.

Infrastructure, from the repository root:

```bash
docker compose up -d
docker compose ps
```

Backend:

```bash
cd backend
python -m venv .venv
# Activate .venv for the current shell
python -m pip install -r requirements.txt
alembic upgrade head
python -m pytest -q
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Electron kiosk development:

```bash
cd frontend
npm run electron:dev
```

## Deliberate non-implementation

The following still require implementation:

- Pydantic request/response schemas and complete CRUD/API routes
- Authentication, authorization enforcement, and staff permission middleware
- Borrowing transaction services and concurrency/availability handling
- Face capture, recognition, liveness detection, hardware integration, encryption, and key management
- Gemini calls, prompt execution, RAG pipelines, and recommendation services
- Redis cache/session integration
- ETL jobs for dimensions, daily facts, popularity snapshots, and materialized-view refresh
- Dashboard UI and BI-tool deployment
- ML training pipelines and artifact storage integration
- PostgreSQL roles, restricted views, row/column security, partitioning, backups, CI/CD, and production deployment

## Recommended implementation sequence

1. Validate both migrations against a disposable PostgreSQL 16 instance and add live integration tests.
2. Add Pydantic schemas and service-layer transaction boundaries.
3. Implement authentication/authorization and privacy enforcement before exposing sensitive models.
4. Implement thin CRUD/API routes over services.
5. Add event emission and AI/search/recommendation attribution consistently.
6. Implement idempotent analytics refresh jobs and approved materialized views.
7. Connect frontend clients and build dashboard views.
8. Add CI, backups, observability, security controls, and production configuration.

## Before submitting changes

- Import every new model through `app.models` so Alembic metadata sees it.
- Review migration upgrade and downgrade manually.
- Run `python -m pytest -q` from `backend`.
- Run `npm run build` from `frontend` for frontend changes.
- Update the database/dashboard documentation when changing tables, metrics, event semantics, or fact grain.
- Preserve unrelated worktree changes and never commit secrets, `.env`, database dumps, virtual environments, or build artifacts.
