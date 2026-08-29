# Data dictionary

## Conventions

Unless noted, `id` is PostgreSQL UUID, `created_at`/`updated_at` are non-null `timestamptz`, and mutable business rows may have nullable `deleted_at`. `*_id` is a UUID FK. `JSONB` columns contain only flexible metadata. Event, audit, consent, assignment, and telemetry facts are retained rather than soft deleted.

| Table | Purpose | Important columns (type; nullability; FK) | Research significance |
|---|---|---|---|
| users | Operational identity | email/password_hash/full_name varchar NN; student_code varchar UQ; typed status | Repeat visits and circulation; exclude from anonymized exports |
| user_preferences / user_favorite_genres | Queryable and flexible preferences | user_id FK NN; genre_id FK; input/language; JSONB accessibility | Preference-based cohorts |
| research_participant_profiles | Separately protected demographics | anonymous_code varchar UQ; user_id FK nullable; demographics JSONB | Avoids demographics in operational identity |
| consent_records | Versioned permission facts | user_id FK NN; versions; granted flags/times; retention_until | Consent-as-of-event-time |
| data_subject_requests | Erasure/export/anonymization workflow | user_id FK nullable; request/status/timestamps | Governance evidence |
| face_profiles | Secure biometric template locator | user_id FK; encrypted bytes or secure reference; model/version/quality/revocation | Enrollment quality without raw images |
| devices / library_locations | Kiosk/web/mobile context | type/status/version/location/last_seen | Device and location comparisons |
| user_sessions | Complete visit envelope | user/device FKs nullable; channel; start/end/duration/exit | Duration, visits, funnels, conversion |
| authentication_events | One authentication attempt | session/user/device FKs; method/result/confidence/latency/attempt/time | Face success, retry and latency |
| interaction_events | Immutable behavioral facts | session FK NN; event_type/time; entity; input; latency; JSONB | Canonical funnel and user journey |
| publishers / authors / genres | Normalized catalog dimensions | bounded names; UUID PKs | Book cohorts |
| books | Bibliographic work | ISBN UQ; title; year/language/publisher; metadata JSONB | Work-level analysis |
| book_authors / book_genres | Many-to-many associations | composite PK/FKs; author_order | No duplicated strings; duplicates rejected |
| shelves / book_copies / ebooks | Physical/digital holdings | book/location/shelf FKs; barcode UQ; status/access | Availability and circulation |
| ebook_access_events | Digital usage facts | ebook/session/user FKs; time/outcome | Physical vs digital outcomes |
| search_queries | Submitted and interpreted query | session/user FKs; raw/normalized text; method/type/time/latency/count/success | Search effectiveness |
| search_results | Ranked result exposure | query/book FKs; positive unique rank; scores; convenience action timestamps | Rank and conversion |
| ai_requests | Model invocation telemetry | session/user FKs; feature/provider/model/prompt version; tokens/cost/status/latency | Cost, errors and model comparison |
| ai_request_contents | Controlled optional AI text | ai_request FK UQ; redacted text or encrypted reference; retention | Keeps sensitive content isolated |
| documents / document_chunks | RAG source registry | book FK nullable; hash/source; chunk order/text/external embedding reference | Versioned retrieval units; no large vectors |
| rag_requests / rag_retrieved_items | Retrieval execution and ranking | AI/search FKs; timing/count; book/chunk; rank/score/context/relevance | Precision, latency and ranking |
| recommendation_runs / recommendation_items | One ranked recommendation output | session/user/AI FKs; trigger/model; book/rank/score; convenience timestamps | Impressions, CTR, attribution and model tests |
| game_sessions / game_questions / game_answers | Mini-game journey | session/user/AI FKs; counts/status; secure answer hash; correctness/response time | Participation and treatment effects |
| borrowing_records | Physical circulation fact | user/copy/session/source FKs; borrow/due/return; status/channel/auth | Duration, compliance and causal attribution |
| return_events | Return processing fact | borrowing/device FKs; time/condition/latency | Return journey and performance |
| notifications / return_reminders | Delivery and reminder treatment | user/loan FKs; schedule/send/open/status; sequence/due offset | Reminder effectiveness |
| surveys / survey_questions | Versioned instruments | version; question code/type/order/options/scales/construct | Evolving validated constructs |
| survey_responses / survey_answers | Submitted instruments | survey/session/user or anonymous code; typed answer slots | Satisfaction and intention to reuse |
| research_studies / experiment_groups | Study definitions | question/hypothesis/version/dates/status; named arms | Experiment provenance |
| research_participants / participant_assignments | Anonymous enrollment and arm history | study/consent/group FKs; anonymous code; join/withdraw/assignment times | A/B cohorts without exposing users |
| system_performance_logs | Application request telemetry | service/endpoint/time/status and component latencies | P50/P95/P99 and bottlenecks |
| system_errors | Application error facts | session/device FKs; component/code/severity/times | Error frequency/rate |
| audit_logs | Immutable sensitive-action trail | actor nullable; action/target/time/IP/details/request | Access, consent, biometric and export accountability |

`RecommendationItem.clicked_at` and similar fields and `SearchResult.clicked` are convenience projections. Behavioral analysis must use timestamped `interaction_events` as the source of truth.
