# Phase 2 API structure

Responses use `{ success, message, data }`; validation failures use `{ success: false, message, error }`.

| Route | Purpose | Status |
|---|---|---|
| `GET /health` | Lightweight app health | Working |
| `GET /api/v1/health` | App, safe DB status, environment and API version | Working |
| `POST /api/v1/kiosk/sessions/start` | Start anonymous kiosk flow | Mock |
| `POST /api/v1/kiosk/sessions/{id}/end` | End flow and return next state `IDLE` | Mock |
| `POST /api/v1/face/verify/mock` | Success, unknown, low-confidence, timeout and error transitions | Mock |
| `POST /api/v1/conversations/start` | Start kiosk conversation | Mock |
| `POST /api/v1/conversations/{id}/messages` | Accept a user message | Mock |
| `POST /api/v1/ai/answer/mock` | AI-shaped deterministic answer | Mock |
| `GET /api/v1/book-categories/mock` | Curated categories | Mock |
| `GET /api/v1/suggested-books/mock` | Simple category suggestions | Mock |
| `GET /api/v1/surveys/active/mock` | Active survey | Mock |
| `POST /api/v1/surveys/{id}/responses/mock` | Accept response shape | Mock; no persistence |
| `GET /api/v1/admin/dashboard/mock` | Staff dashboard metrics | Mock |
| `GET /api/v1/admin/status` | Module delivery status | Static |

Older Phase 2 mock aliases remain temporarily for compatibility. No endpoint performs real authentication, recognition, parsing, RAG, provider calls or production persistence.

## Phase 3 runtime endpoints

- `GET /api/v1/health/db`: executes `SELECT 1`; returns structured 503 when unavailable.
- `POST /api/v1/kiosk/sessions/{id}/events`: persists a kiosk event.
- `POST /api/v1/face/enroll`: validated multipart enrollment; persists template reference/profile and event.
- `POST /api/v1/face/verify`: validated frame, provider verification, auth log, session identity and event.
- `POST /api/v1/voice/transcribe`: validated audio, configured STT provider and optional voice message.
- `POST /api/v1/voice/browser-transcript`: persists Web Speech transcript and question event.
- `POST /api/v1/ai/answer`: persists user message, AI request/response/message and answer event.
- `POST /api/v1/knowledge/chunks/search/mock`: database text-match retrieval bridge.
- `GET /api/v1/book-categories` and `/api/v1/suggested-books`: database-backed suggestions.
- `GET /api/v1/surveys/active` and `POST /api/v1/surveys/{id}/responses`: database-backed survey flow.

Session, conversation, event, survey and AI records are real PostgreSQL writes. Face matching, STT, AI generation and knowledge retrieval quality remain provider/mock implementations.
