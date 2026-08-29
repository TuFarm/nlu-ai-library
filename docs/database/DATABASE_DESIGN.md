# Database design

## Architecture

The schema separates operational entities (identity, catalog, circulation) from append-only behavioral and performance facts, and connects both through UUID foreign keys. All times are timezone-aware. Mutable business records use `created_at`, `updated_at`, and, where meaningful, `deleted_at`; factual logs intentionally have no soft-delete field.

Controlled vocabularies use Python `StrEnum` mapped to bounded `VARCHAR` plus SQLAlchemy validation rather than PostgreSQL native ENUM. This makes vocabulary evolution safer while retaining typed application code. Flexible metadata uses PostgreSQL JSONB only where attributes are genuinely variable. Biometric bytes, prompts, and research demographics are never stored on `users`.

## Domains and relationships

- Identity/privacy: `users`, preferences, favorite genres, participant profiles, consent history, and data-subject requests. Consent rows are versioned facts; `(user_id, granted_at)` resolves permission at event time.
- Face/auth/device/session: secure face template/reference records, authentication attempts, devices, locations, sessions, and immutable interaction events reconstruct identification and journeys.
- Catalog: books have normalized publishers, ordered authors, genres, copies, shelves, locations, and ebook editions.
- Discovery/AI: search queries preserve interpretations and ranked results. AI requests preserve model/prompt versions, tokens, cost and latency. Sensitive content is optional, redacted, separately retained, and auditable.
- RAG/recommendation/game: requests and ranked items retain model output; actions are primarily facts in `interaction_events`. Convenience timestamps/flags are projections and must not replace events.
- Circulation: a physical loan references a copy. Nullable source search/recommendation FKs and `attribution_source` distinguish direct, browse, search, and recommendation origins. Ebook access is a separate fact.
- Notifications/surveys/research: reminders link delivery to a loan; versioned survey instruments avoid hard-coded columns; anonymous study participants and time-bounded assignments support A/B tests.
- Telemetry/security: application-level latency and errors support research. Infrastructure monitoring remains the responsibility of an external observability platform. Audit logs are append-only.

## Integrity and indexing

Checks reject negative latency/token/cost/ranks, invalid score ranges, impossible game counts, and reversed date intervals. Composite unique constraints prevent duplicate ranked items and associations. High-value indexes include session/event time, event type/time, user/session time, search/result rank, recommendation/rank, user/loan status, book/borrow time, and service/performance time.

`RESTRICT` protects research and circulation facts; `SET NULL` removes direct identity/device linkage while preserving facts. `CASCADE` is limited to ownership-only mutable associations such as book-author links and document chunks.

## Privacy and retention

`face_profiles` accepts either an encrypted template or an external vault reference, never a raw photograph. Encryption, key rotation, access control, and vault lifecycle belong to the security service—not fake database encryption. Consent, revocation, retention deadlines, erasure/anonymization requests, and sensitive actions are independently recorded. Research exports should use `anonymous_participant_code` and enforce consent-as-of-event-time.

## Migration

The initial Alembic revision creates the reviewed registered metadata in dependency order and drops it in reverse order. This metadata-driven initial revision is appropriate while the repository has no deployed schema; future revisions must use explicit Alembic operations so historical migrations remain immutable.
