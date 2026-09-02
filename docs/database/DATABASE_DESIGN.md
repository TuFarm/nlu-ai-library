# Thiết kế database cho AI Library Receptionist Kiosk

## Phạm vi

Đây là trợ lý lễ tân thư viện bằng AI, không phải hệ thống quản lý thư viện. Trường/thư viện đã có hệ thống quản lý sách và lưu thông riêng. Vì vậy schema chỉ giữ 24 bảng cần cho nhận diện FaceID, phiên kiosk, hỏi đáp dựa trên tài liệu, gợi ý sách đơn giản, khảo sát và báo cáo nghiên cứu cơ bản.

Các bảng tác giả, nhà xuất bản, bản sao sách, kệ, mượn/trả, recommendation engine, experiment framework và data warehouse đã bị loại. Nếu cần liên kết sách, `suggested_books.external_book_id` trỏ logic đến mã sách của hệ thống hiện hữu; database này không sao chép nghiệp vụ catalog/circulation.

## Nguyên tắc

- UUID cho khóa chính; timestamp có timezone; FK, index, unique và check constraint ở database.
- Bảng mutable dùng `created_at`, `updated_at`, và `deleted_at` khi cần.
- Log/fact append-only không có `deleted_at`: FaceID log, interaction event, AI request/response/feedback, suggestion log, survey response/answer.
- Không lưu ảnh khuôn mặt thô. `face_profiles` chỉ chứa template mã hóa hoặc secure reference.
- `face_authentication_logs.user_id` nullable vì khuôn mặt không nhận diện được chưa có danh tính. `UNKNOWN_FACE` phải ghi `user_id=NULL`.
- `user_sessions.user_id` nullable để hỗ trợ phiên ẩn danh.
- Không có cột `student_year`. Backend tính `current_year - admission_year + 1`; năm nhập học thiếu hoặc ở tương lai trả `None`.

## Luồng backend dự kiến

1. Tạo `user_session` khi có người tiếp cận kiosk.
2. Thử FaceID và luôn ghi `face_authentication_logs`; nếu thành công mới gắn user vào session.
3. Tạo conversation và lưu user message.
4. Lấy chunk từ document đang active/processed.
5. Chọn prompt version, tạo AI request, gọi provider và lưu AI response/message.
6. Hiển thị câu trả lời, gợi ý sách tùy chọn, rồi lưu feedback/survey nếu người dùng đồng ý.
7. Job định kỳ tổng hợp raw logs thành `daily_report_metrics` mà không xóa hoặc thay raw data.

## Luồng frontend dự kiến

Kiosk: Home → Face Recognition → AI Chat → Book Suggestion (tùy chọn) → Survey (tùy chọn).

Admin: Knowledge Upload → Basic Dashboard. Các trang hiện chỉ là placeholder; chưa có upload, FaceID hay AI call thật.

## Tri thức tài liệu

Upload tạo `knowledge_source`; parser tạo một hoặc nhiều `knowledge_document`; chunker tạo các `knowledge_chunk` có thứ tự, trang/sheet và metadata. RAG chỉ truy vấn document active đã xử lý thành công. Embedding/pgvector chưa được thêm vì vector stack chưa được chọn.

## Hội thoại và cải tiến AI

Message gần đây có thể làm context ngắn hạn. Conversation cũ chỉ được chọn lọc để phân tích FAQ, không trở thành tri thức đúng mặc định. Feedback giúp tìm câu trả lời, prompt hoặc tài liệu yếu. Prompt được version hóa để so sánh có kiểm soát.

## Báo cáo nghiên cứu

Raw session, FaceID, interaction, AI, suggestion và survey logs hỗ trợ thống kê nhận diện, mức sử dụng, độ trễ, lỗi, mức hữu ích và hài lòng. `daily_report_metrics` là cache tổng hợp theo ngày, không thay thế raw facts.
