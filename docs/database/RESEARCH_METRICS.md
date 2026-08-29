# Research metrics

All rates should define a study window, eligible population, and denominator before publication. Event-based measures use `interaction_events`; PostgreSQL examples use `FILTER`, `percentile_cont`, and `date_trunc`.

| # | Metric and definition | Required tables / columns or events | Suggested SQL calculation |
|---:|---|---|---|
| 1 | Face success rate: successful face attempts / face attempts | authentication_events method,result | `count(*) FILTER (WHERE result='SUCCESS') / count(*)` filtered to FACE |
| 2 | Face average latency | authentication_events processing_time_ms | `avg(processing_time_ms)` filtered to FACE |
| 3 | Face retry rate: sessions with attempt >1 / authenticated sessions | authentication_events session_id,attempt_number | conditional distinct-session counts |
| 4 | Average session duration | user_sessions start/end,duration | `avg(coalesce(duration_seconds, extract(epoch from ended_at-started_at)))` |
| 5 | Sessions/day/week/month | user_sessions started_at | `count(*) GROUP BY date_trunc(period,started_at)` |
| 6 | Returning-user frequency | user_sessions user_id,started_at | visits after each user's first visit per time window |
| 7 | Searches/session | search_queries session_id | query count grouped by session, then average |
| 8 | Voice vs text usage | search_queries input_method | counts grouped by input_method |
| 9 | Voice vs text success | search_queries input_method,successful_search | average success boolean by method |
| 10 | Search latency | search_queries processing_time_ms | average/percentiles by type and method |
| 11 | Zero-result rate | search_queries result_count | fraction where result_count=0 |
| 12 | Search→click conversion | search_queries/results; SEARCH_RESULTS_DISPLAYED,BOOK_CLICKED | distinct clicked queries / displayed queries |
| 13 | Search→borrow conversion | borrowing_records source_search_id | distinct sourced searches / eligible searches |
| 14 | Recommendation impressions | RECOMMENDATION_DISPLAYED + entity_id | count displayed events |
| 15 | Recommendation CTR | displayed and RECOMMENDATION_CLICKED | clicked item events / displayed item events |
| 16 | Recommendation→borrow | borrowing_records source_recommendation_item_id | attributed loans / displayed items |
| 17 | Recommendation acceptance | recommendation click/save/borrow events | distinct items with any acceptance / impressions |
| 18 | Recommendation rank effectiveness | recommendation_items rank; click/borrow events | outcome rate or mean reciprocal rank by rank_position |
| 19 | AI response latency | ai_requests latency_ms | average/percentiles by feature/model/version |
| 20 | AI token consumption | ai_requests input/output/total_tokens | sums and averages grouped by feature/model |
| 21 | AI request cost | ai_requests estimated_cost,currency | sum cost grouped by currency/model/feature |
| 22 | AI error rate | ai_requests status,error_code | failed/timeout requests / all requests |
| 23 | RAG retrieval latency | rag_requests retrieval_time_ms | average/percentiles |
| 24 | RAG retrieval ranking | rag_retrieved_items rank,score,relevance_label | precision@k, MRR, score distribution |
| 25 | Game participation | game_sessions; eligible user_sessions | distinct game sessions / eligible sessions |
| 26 | Game completion | game_sessions completion_status | completed / started |
| 27 | Game vs non-game duration | game_sessions,user_sessions duration | left join and compare grouped averages |
| 28 | Game vs non-game borrowing | game_sessions,borrowing_records session_id | session loan rate grouped by game existence |
| 29 | Borrowing frequency | borrowing_records user_id,borrowed_at | loans per user and time period |
| 30 | Average borrowing duration | borrowing_records borrowed_at,returned_at | average returned_at-borrowed_at |
| 31 | Return compliance | borrowing_records returned_at,due_at | fraction returned_at<=due_at |
| 32 | Overdue rate | borrowing_records due/return/status | loans returned late or open past due / due loans |
| 33 | Reminder effectiveness | return_reminders,notifications,borrowing_records | compare on-time returns by reminder delivered/opened and sequence |
| 34 | User satisfaction | survey questions/answers construct_name,numeric_value | mean/median validated satisfaction items |
| 35 | Intention to reuse | survey_questions construct_name + answers | aggregate items tagged `intention_to_reuse` |
| 36 | Library circulation impact | borrowing_records + experiment assignments/time | pre/post or treatment/control loans per participant-time |
| 37 | System API latency | system_performance_logs response_time_ms | average grouped by endpoint/service |
| 38 | P50/P95/P99 latency | system_performance_logs response_time_ms | `percentile_cont(ARRAY[.5,.95,.99]) WITHIN GROUP` |
| 39 | System error rate | system_errors + performance logs | errors or 5xx requests / total requests, by window |
| 40 | Cost-benefit | AI cost, circulation, sessions, outcomes | total AI cost / incremental loans, engaged users, or satisfaction gain |

## Journey reconstruction

Order `interaction_events` by `(session_id, event_timestamp, created_at)` and join entity IDs to searches, recommendations, books, loans, AI/RAG requests, games, and surveys. The intended funnel is presence → authentication → welcome → game decision → search → RAG/AI → recommendation → book interaction → borrow authentication → loan → reminder → return → survey. Borrow attribution uses explicit source FKs; experiment analysis uses assignment validity at the event timestamp and consent validity at that same timestamp.
