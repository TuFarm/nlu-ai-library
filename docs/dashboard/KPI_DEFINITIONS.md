# KPI definitions

`dashboard_metrics` is the authoritative metric catalog. A seeded metric should include its formula, unit, owner, refresh SLA, source tables and category. Dashboards must reference the catalog rather than redefining formulas.

| KPI | Governed definition | Primary source | Refresh |
|---|---|---|---|
| Active users | Distinct identified users with a session | fact_daily_library_usage | 15 min |
| User growth | New registrations versus previous comparable period | users, dim_date | Daily |
| Borrow count | Loans whose `borrowed_at` falls in period | fact_borrowing | 15 min |
| Return compliance | Returns on/before due date divided by due loans | borrowing_records | Daily |
| Search success | Successful searches divided by total searches | fact_search | 15 min |
| Search conversion | Search-attributed loans divided by searches | fact_search | Daily |
| Recommendation CTR | Clicks divided by impressions | fact_recommendation | 15 min |
| Recommendation borrow rate | Attributed loans divided by impressions | fact_recommendation | Daily |
| AI success rate | Successful AI requests divided by requests | fact_ai_usage | 5 min |
| AI cost | Sum estimated cost, never mixing currencies | fact_ai_usage | 5 min |
| FaceID success | Successful FACE attempts divided by FACE attempts | fact_authentication | 5 min |
| Game completion | Completed games divided by started games | fact_game | 15 min |
| Satisfaction | Mean score for governed satisfaction construct | fact_survey | Daily |
| Occupancy | Occupancy divided by reading-room capacity | location_traffic_snapshots | 5 min |

Rate denominators must be non-zero and eligibility rules explicit. Currency, timezone, cohort, consent window and late-arrival policy are mandatory dashboard metadata.
