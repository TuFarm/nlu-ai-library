# Service layer

Services are integration boundaries, not repositories yet. Route handlers own deterministic mock payloads for Phase 2.

- `user_service`: pure student-year calculation.
- `session_service`: future anonymous/identified kiosk lifecycle.
- `face_service`: future consent, enrollment, liveness and identity resolution. Unknown identity remains nullable.
- `knowledge_service`: future validation, storage, extraction, chunking and processing state.
- `rag_service`: future retrieval over active `knowledge_chunks`; pgvector is optional and not selected.
- `ai_service`: future Gemini, prompt versioning, RAG context, redaction and persistence.
- `book_suggestion_service`: category-based suggestions only, never a catalog replacement.
- `survey_service`: future submissions and satisfaction metrics.
- `report_service`: future idempotent daily aggregation and summaries.

Replace each mock route by calling its service without changing the public response envelope.
