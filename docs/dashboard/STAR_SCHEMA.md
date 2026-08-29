# Analytics star schema

The application database contains dashboard aggregates now and provides the contract for a future warehouse.

| Dimension | Business key/source | Purpose |
|---|---|---|
| dim_date | full_date | Calendar, holiday, fiscal and academic comparison |
| dim_time | full_time | Hourly traffic, business/peak periods |
| dim_user | pseudonymized user | Cohort, retention and academic segmentation |
| dim_book | books | Stable bibliographic attributes |
| dim_device | devices | Kiosk/channel and software analysis |
| dim_location | locations/shelves/rooms | Library-floor-zone heatmaps |
| dim_ai_model | ai_models | Provider, version, capabilities and pricing |
| dim_genre | genres | Subject demand |

| Atomic fact | Grain | Measures |
|---|---|---|
| fact_session | One session | duration, identified flag, outcome |
| fact_borrow | One loan lifecycle event | loan/return/overdue/renewal/duration |
| fact_search | One query | latency, results, click and borrow outcome |
| fact_recommendation | One item impression | rank, score, click/save/borrow |
| fact_ai | One request | latency, tokens, cost, status |
| fact_game | One game/question answer | completion, score, response time |

Application `fact_*` tables are daily aggregate marts, not substitutes for these future atomic warehouse facts. Their declared grain is enforced by unique constraints.
