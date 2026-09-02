# Changelog database redesign

## 2026-09-02 — Tối ưu phạm vi AI kiosk

- Thời gian: 2026-09-02 22:27:09 +07:00 (Asia/Saigon).
- Lý do: trường đã có Library Management System; project chỉ là AI Library Receptionist/Kiosk Assistant phục vụ FaceID, hỏi đáp RAG, gợi ý đơn giản, khảo sát và nghiên cứu cơ bản.
- Phạm vi cũ: 92 bảng gồm catalog/circulation, research experiments, dashboard facts, warehouse và ML lineage.
- Phạm vi mới: đúng 24 bảng AI kiosk được liệt kê trong data dictionary.

### Removed

Authors, publishers, genres, books/book copies, shelves, locations/ebooks, borrowing/return, search/ranking, RAG request telemetry nâng cao, recommendation runs/items, games, notifications, consent/research experiments, audit/system telemetry, calendar/time dimensions, dashboard facts/configuration, staff/RBAC, academic dimensions, warehouse và ML metadata.

### Kept/refactored or added

Users/preferences, FaceID profiles/logs, devices/sessions/events, knowledge source-document-chunk, conversation-message, AI request-response-feedback, prompt versions, book category/suggested book/log, survey/question/response/answer và daily metrics.

### Files

- Models: thay `schema.py`, xóa `analytics.py` và `enums.py`, cập nhật registry.
- Migration: xóa hai revision cũ; tạo `20260902_0001_ai_kiosk_schema.py`.
- Backend: route registry/domain placeholders, minimal Pydantic status schema, sáu service boundaries và student-year helper.
- Frontend: route flow và bảy page/component placeholders theo kiosk/admin.
- Documentation: viết lại design/dictionary/ERD, thêm AI-vs-reporting và changelog; xóa tài liệu warehouse không còn đúng phạm vi.
- Tests: viết lại theo 24 bảng, relationship, nullable identity, constraints và helper.

### Assumptions and risks

- Pre-production, không có schema deployed cần giữ backward compatibility.
- Hệ thống thư viện hiện hữu sẽ cung cấp optional external book ID.
- Chưa chọn vector store; chunk được lưu trước, embeddings thêm bằng migration tương lai.
- Chưa có consent enforcement, encryption/key management, file parsing, AI provider, FaceID, ETL scheduler hoặc CRUD.
- Migration cần được chạy integration trên PostgreSQL 16 trước demo/triển khai.
