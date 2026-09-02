# Dữ liệu AI và dữ liệu báo cáo

> The AI does not directly retrain itself from every record in the database. Instead, the system stores uploaded knowledge sources, conversation context, feedback, and prompt versions so that the AI can retrieve relevant information, personalize basic responses, and support future improvements.

AI không “tự học” mất kiểm soát từ mọi record. Database cung cấp persistence cho RAG, context hội thoại ngắn hạn, memory dài hạn được chọn lọc, prompt versioning, feedback loop, trả lời theo tài liệu và đánh giá hệ thống.

## Dữ liệu phục vụ AI response/cải tiến

- `knowledge_sources`, `knowledge_documents`, `knowledge_chunks`: nguồn RAG chính.
- `conversation_messages`: context ngắn hạn; chỉ chọn lọc cho phân tích lâu dài.
- `ai_feedback`: phát hiện câu trả lời sai/không hữu ích và ưu tiên cải tiến.
- `prompt_versions`: prompt có phiên bản, không sửa lịch sử tùy tiện.
- `user_preferences`: cá nhân hóa cơ bản.
- `face_profiles`: chỉ định danh, không phải tri thức trả lời.
- `suggested_books`: gợi ý đơn giản theo category/preference.

## Dữ liệu chủ yếu cho nghiên cứu/báo cáo

- `user_sessions`: lượt dùng, ẩn danh/đã nhận diện, thời lượng.
- `interaction_events`: số câu hỏi, câu trả lời, yêu cầu nhân viên và funnel cơ bản.
- `face_authentication_logs`: success, unknown, latency và retry.
- `ai_requests`, `ai_responses`: volume, trạng thái, độ trễ và grounded answer.
- `book_suggestion_logs`: impression, click và feedback.
- `surveys`, `survey_questions`, `survey_responses`, `survey_answers`: hài lòng, ý định tái sử dụng, tính hữu ích và khả năng giảm nhu cầu hỏi lễ tân.
- `daily_report_metrics`: tổng hợp theo ngày cho dashboard cơ bản.

Một bảng có thể hỗ trợ cả vận hành và đánh giá, nhưng điều đó không cho phép dùng dữ liệu cá nhân hoặc hội thoại để huấn luyện nếu chưa có consent, anonymization và quy trình phê duyệt.
