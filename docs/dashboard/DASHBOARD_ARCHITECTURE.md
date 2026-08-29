# Dashboard architecture

## Layers

1. Operational tables remain the authoritative transaction/event store.
2. PostgreSQL materialized views provide low-latency near-real-time summaries.
3. Daily fact tables provide stable, auditable dashboard aggregates with `refreshed_at` and `source_watermark`.
4. `dim_date` and `dim_time` provide calendar, academic, fiscal, holiday, hourly, business-hour, and peak-hour slicing.
5. A read-only BI role exposes curated facts/views to Power BI, Grafana, Metabase, and Superset without granting biometric, prompt-content, or direct identity access.

Refresh jobs must be idempotent: aggregate a closed time window into staging, validate counts, then upsert the relevant grain in one transaction. Refresh the current day every 5–15 minutes, finalize yesterday nightly, and rebuild late-arriving windows for seven days. Store the maximum source event timestamp in `source_watermark`.

## Executive dashboard

Library Overview uses daily usage and borrowing facts; Borrow/Search Trend uses borrowing/search facts; Recommendation CTR uses recommendation facts; AI Usage/Cost uses AI facts; User Growth uses daily usage; Reading Heatmap uses location traffic; Top Books/Genres/Authors use popularity and materialized views; FaceID Success uses authentication facts; Session Funnel uses interaction-event materialization; Survey Satisfaction uses survey facts.

## Research dashboard

Experiment Results and A/B Test join anonymous assignments to fact/event outcomes. Recommendation Accuracy uses recommendation facts and RAG relevance. Search Efficiency and Voice vs Text use search facts. Game Effectiveness joins game and borrowing facts by experimental cohort. Borrow Conversion uses attributed search/recommendation facts. Retention/cohort/survival analysis should run from de-identified session and borrowing extracts whose consent and assignment were valid at event time.

## Geographic and academic analytics

Faculties, majors, courses, enrollments, academic year, student year and semester support university reporting. Libraries, floors, zones, shelves, kiosks, reading rooms and time-bucketed traffic snapshots support heatmaps. Suppress small academic/geographic cells to reduce re-identification risk.

## Dashboard configuration and alerts

Metrics have governed names, formulas, owners and refresh frequencies. Dashboards contain widgets, responsive layouts, filters, saved filters and user preferences. Alert rules evaluate governed metrics and retain immutable trigger/acknowledgement/resolution history for AI latency, recommendation CTR, FaceID failure, overdue rates and application/database health.

## Dashboard indexes

Facts index `date_key`; composite indexes cover `(date_key, location_id)`, popularity `(date_key, score)`, location traffic `(date_key, location_id)`, staff activity `(staff_id, occurred_at)`, and AI request model/prompt FKs. Production rollouts should inspect `pg_stat_statements` before adding tool-specific indexes. Partition high-volume event/performance tables monthly when volume justifies it.

## New-table inventory

| Domain | Tables | Why they exist |
|---|---|---|
| Conformed time | `dim_date`, `dim_time` | Consistent calendar, academic, fiscal, holiday, hour and peak-period slicing |
| AI governance | `ai_models`, `prompt_templates` | Versioned pricing/capability and prompt comparisons; `ai_requests` now has optional FKs while legacy text fields remain |
| Staff/RBAC | `departments`, `staff`, `roles`, `permissions`, `staff_roles`, `role_permissions`, `staff_activities` | Authorization structure and measurable staff work without overloading users/audit logs |
| Academic | `faculties`, `majors`, `courses`, `student_academic_profiles`, `course_enrollments` | University reporting by organization, program, course, year and semester |
| Geography | `reading_rooms`, `location_traffic_snapshots` | Floor/zone/room/kiosk occupancy and usage heatmaps |
| Aggregate marts | `fact_daily_library_usage`, `fact_borrowing`, `fact_search`, `fact_recommendation`, `fact_ai_usage`, `fact_game`, `fact_authentication`, `fact_survey` | Stable daily dashboard grains that avoid repeated joins over operational facts |
| Popularity | `book_popularity_snapshots` | Reproducible dated Top-N rankings rather than mutable lifetime counters |
| KPI/alerts | `dashboard_metrics`, `alert_rules`, `alert_history` | Governed formulas and traceable operational threshold evaluation |
| Dashboard UX | `dashboards`, `dashboard_widgets`, `widget_layouts`, `widget_filters`, `saved_filters`, `user_dashboard_preferences` | Shareable and personalized BI presentation without schema changes |
| ML lineage | `ml_datasets`, `dataset_versions`, `ml_experiments`, `feature_sets`, `training_runs`, `evaluation_metrics` | Reproducible, privacy-aware datasets, features, training and offline evaluation |
