# Data dictionary

Mọi `id` là UUID. `created_at`/`updated_at` là timezone-aware; `deleted_at` chỉ có trên mutable business records.

| Table | Mục đích | Cột chính và ràng buộc |
|---|---|---|
| users | Danh tính cơ bản | student_code/email unique nullable; faculty, major, admission_year≥1990; không lưu student_year |
| user_preferences | Cá nhân hóa nhẹ | user_id unique FK; category/topics/style/input/note |
| face_profiles | Template định danh | user FK; encrypted bytes hoặc secure ref bắt buộc; quality 0–1; không ảnh thô |
| face_authentication_logs | Mỗi lần FaceID | user/session/device nullable; result; attempt>0; latency≥0; confidence 0–1 |
| devices | Kiosk | device_code unique; name/location/status |
| user_sessions | Một lượt kiosk | user/device nullable; start/end/duration; identified; exit_reason |
| interaction_events | Log tương tác cơ bản | nullable session/user/device; type/time/input/summary/success |
| knowledge_sources | File/link upload | type, file metadata, URL/path, uploader, processing status |
| knowledge_documents | Tài liệu logic | source FK; title/type/language/version; active/status |
| knowledge_chunks | Đơn vị RAG | document FK; unique index; text/page/sheet/JSONB; index≥0 |
| conversations | Phiên hội thoại | nullable session/user; start/end/status |
| conversation_messages | Message context | conversation FK; sender/text/input/time/intent |
| prompt_versions | Prompt bất biến có version | unique name+version; version>0; text/reason/active |
| ai_requests | Lần gọi AI | conversation/message/prompt FKs nullable; type/model/tokens/latency/status; số liệu≥0 |
| ai_responses | Kết quả AI | request FK; optional AI message; text/summary/grounded/confidence 0–1 |
| ai_feedback | Feedback câu trả lời | response FK; optional user; rating 1–5/helpful/correct/comment |
| book_categories | Nhóm gợi ý đơn giản | category_name unique; description |
| suggested_books | Danh sách gợi ý, không phải catalog | optional category/external ID; title/author/summary/source |
| book_suggestion_logs | Lịch sử impression/click | nullable user/session/category/book; shown time; rating 1–5 |
| surveys | Phiên bản khảo sát | unique name+version; version>0; description/active |
| survey_questions | Câu hỏi có thứ tự | survey FK; unique order; order>0; type/text |
| survey_responses | Một submission | survey FK; nullable user/session; submitted time |
| survey_answers | Câu trả lời typed đơn giản | response/question FKs unique; text hoặc numeric |
| daily_report_metrics | Aggregate theo ngày | report_date unique; counts≥0; satisfaction 1–5; AI latency≥0 |
