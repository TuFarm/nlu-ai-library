# Implementation log

## 2026-09-03 — Phase 2 foundation

- Preserved the optimized 24-table kiosk schema and existing migration.
- Added standard API success/validation-error envelopes and safe database health reporting.
- Added domain Pydantic schemas, session/book service boundaries, and expanded service TODOs.
- Added mock endpoints for user, session, FaceID, knowledge, conversation, AI, suggestions, surveys and reports.
- Added endpoint/helper tests.
- Rebuilt the React UI around a responsive app shell with complete kiosk and admin route coverage.
- Added interactive FaceID simulation, mock chat, book filtering and survey completion flow.
- Added admin metrics, upload placeholder, logs, users, surveys, reports and polished incomplete states.
- Added an environment-aware API client and documented frontend fallback mock usage.

Intentionally not implemented: authentication/RBAC, camera access, biometric processing, Gemini, RAG, parsers, embeddings, real upload/persistence, production charts, catalog or circulation.

Next: introduce service transactions and repositories, consent/auth policy, storage/parser design, selected retrieval stack, Gemini execution and integration tests against disposable PostgreSQL.

## 2026-09-03 — Admin/Kiosk architecture correction

- Split the frontend into `AdminLayout` and fullscreen `KioskLayout`; root now presents both modes.
- Added a reducer-free `useKioskFlow` state controller with inactivity reset and session/conversation context.
- Added dedicated kiosk screens for presence, scan, recognized/unknown identity, welcome, chat, books, survey, thank-you and error.
- Prepared Electron to enter the fullscreen kiosk route through `MemoryRouter` while browsers retain normal URLs.
- Added kiosk session and admin mock routes; aligned conversation route names and added FaceID `next_state` for all mock outcomes.
- Updated psycopg binary requirement for newer Python installers and documented Python 3.12 as the recommended runtime.

Verification: `npm run build` passed (TypeScript and Vite); `git diff --check` passed. Backend tests could not run because this execution environment exposes no `python`, `py`, or `python3` executable.

## 2026-09-03 — Phase 3 kiosk backend runtime

- Added transaction-scoped DB dependency and structured database errors.
- Implemented database-backed kiosk sessions/events, conversations/messages, AI request/response history, face profiles/logs and survey submissions.
- Added multipart face enrollment/verification and voice transcription endpoints with provider isolation.
- Added safe local media validation, randomized filenames, size limits and delete-after-processing default.
- Added browser Web Speech transcript persistence and simple database chunk search.
- Added real database category/book and active-survey reads.
- Added idempotent `scripts/seed_dev.py` for device, user/profile, books, knowledge chunks and survey.
- No migration was required; all writes fit the existing 24-table schema.
- Real local recognition, STT, Gemini and RAG remain isolated placeholders.
- Verification completed with a clean Python 3.12 environment: requirements installed with `psycopg-binary 3.3.5`, 21 tests passed, FastAPI imported 40 routes, Alembic offline SQL compiled, frontend production build passed, and live DB health correctly returned structured 503 because PostgreSQL was not running.
