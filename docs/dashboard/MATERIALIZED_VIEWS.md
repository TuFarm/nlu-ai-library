# PostgreSQL materialized views

Recommended views:

- `mv_daily_usage`: sessions, identified users, duration and conversion by date/location.
- `mv_top_books`: borrow/search/view/recommendation weighted score by rolling window.
- `mv_top_authors`: circulation and engagement through book-author links.
- `mv_search_statistics`: method/type volume, success, zero results, latency and conversion.
- `mv_recommendation_statistics`: impressions, clicks, saves, attributed loans and rank effectiveness.
- `mv_ai_usage`: request status, tokens, cost and latency by model/prompt/feature.
- `mv_faceid_statistics`: attempts, success, retries, confidence and latency by device/time.
- `mv_dashboard_summary`: small executive daily summary assembled from governed facts.

Create a unique index matching each view grain so PostgreSQL can use `REFRESH MATERIALIZED VIEW CONCURRENTLY`. Refresh near-real-time views every 5–15 minutes, popularity hourly, and closed-period summaries nightly. Run an initial non-concurrent refresh after deployment; concurrent refreshes require a populated view and unique index. Serialize refreshes with advisory locks, retain last-success/watermark telemetry, retry failures, and alert when freshness exceeds the KPI SLA.

Do not materialize direct PII, biometric references, raw prompts, free-text errors, or small research cells. Views are deployment-specific SQL and are documented rather than created in the migration so refresh cadence, holiday calendar, timezone, and privacy thresholds can be approved first.
