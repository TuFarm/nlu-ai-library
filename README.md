# Hệ thống Quản lý Thư viện Tích hợp AI

Monorepo cho hệ thống thư viện đại học, gồm backend FastAPI, PostgreSQL, Redis và giao diện React/TypeScript dành cho web lẫn kiosk cảm ứng. Kiến trúc dữ liệu hỗ trợ đồng thời nghiệp vụ thư viện, nghiên cứu khoa học, dashboard quản trị, BI và các quy trình AI/ML trong tương lai.

> Trạng thái hiện tại: nền tảng database và analytics đã được thiết kế đầy đủ; API nghiệp vụ, FaceID, Gemini, Redis client và phần lớn giao diện vẫn là các điểm mở rộng, chưa phải sản phẩm hoàn chỉnh.

## Kiến trúc tổng quan

```text
nlu-library-ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/routes/       # Router FastAPI, hiện chủ yếu là khung
│   │   ├── core/                # Cấu hình, engine và SQLAlchemy Base
│   │   ├── models/              # 92 bảng operational, research và analytics
│   │   └── services/            # Biên tích hợp nghiệp vụ/Gemini
│   ├── alembic/                 # Hai migration database
│   └── tests/                   # Kiểm tra metadata, FK, constraint và model
├── frontend/
│   ├── src/                     # React + TypeScript + React Router
│   └── electron/                # Vỏ ứng dụng kiosk Electron
├── docs/database/               # ERD, data dictionary, research metrics
├── docs/dashboard/              # KPI, star schema, warehouse, materialized views
└── docker-compose.yml           # PostgreSQL 16 và Redis 7
```

### Công nghệ

- Backend: Python, FastAPI, SQLAlchemy 2.x
- Database: PostgreSQL 16, Alembic, UUID, JSONB, INET
- Cache/session infrastructure: Redis 7
- Frontend: React, TypeScript, Vite
- Kiosk desktop: Electron
- AI integration boundary: Gemini API
- Analytics: date/time dimensions, dashboard facts, KPI registry, alerting và ML lineage

## Yêu cầu trước khi cài đặt

- Git
- Docker Desktop hoặc Docker Engine có Docker Compose v2
- Python 3.12 khuyến nghị; Python 3.11 trở lên phù hợp với mã nguồn hiện tại
- Node.js 20 trở lên và npm

Kiểm tra các công cụ:

```bash
git --version
docker --version
docker compose version
python --version
node --version
npm --version
```

Trên Windows, nếu lệnh `python` không tồn tại, thử `py -3.12` và thay `python` trong các lệnh bên dưới bằng lệnh đó.

## Hướng dẫn cài đặt và chạy từng bước

### Bước 1: Lấy mã nguồn

```bash
git clone <repository-url>
cd nlu-library-ai
```

Nếu đã có mã nguồn, mở terminal tại thư mục gốc chứa `docker-compose.yml`.

### Bước 2: Tạo cấu hình backend

Windows PowerShell:

```powershell
Copy-Item backend/.env.example backend/.env
```

macOS/Linux:

```bash
cp backend/.env.example backend/.env
```

Nội dung mặc định:

```dotenv
APP_NAME=NLU AI-Integrated Library Management System
API_V1_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg://ai_library:ai_library_dev@localhost:5432/ai_library
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=
```

Không commit `backend/.env` hoặc API key thật. `GEMINI_API_KEY` có thể để trống vì tích hợp Gemini chưa được triển khai.

Docker Compose đọc file `.env` ở thư mục gốc nếu có. Khi dùng thông số mặc định, không cần tạo file này. Nếu muốn tùy chỉnh container, tạo `.env` tại thư mục gốc:

```dotenv
POSTGRES_DB=ai_library
POSTGRES_USER=ai_library
POSTGRES_PASSWORD=ai_library_dev
POSTGRES_PORT=5432
REDIS_PORT=6379
```

Khi đổi thông tin PostgreSQL ở file gốc, phải cập nhật `DATABASE_URL` trong `backend/.env` tương ứng.

### Bước 3: Khởi động PostgreSQL và Redis

Tại thư mục gốc:

```bash
docker compose up -d
docker compose ps
```

Hai service cần chuyển sang trạng thái `healthy`. Xem log khi có lỗi:

```bash
docker compose logs -f postgres
docker compose logs -f redis
```

### Bước 4: Tạo môi trường Python và cài backend

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Các lệnh backend sau đây phải chạy trong thư mục `backend` và khi virtual environment đang được kích hoạt.

### Bước 5: Tạo database schema bằng Alembic

Đảm bảo PostgreSQL đang chạy, sau đó:

```bash
alembic upgrade head
alembic current
```

Migration hiện có:

1. `20260829_0001`: schema nghiệp vụ và nghiên cứu.
2. `20260829_0002`: analytics, dashboard, AI registry, staff/RBAC và ML metadata.

Kiểm tra SQL mà không thực thi:

```bash
alembic upgrade head --sql
```

Chỉ dùng downgrade trên database phát triển và sau khi đã sao lưu:

```bash
alembic downgrade -1
```

### Bước 6: Chạy kiểm thử backend

```bash
python -m pytest -q
```

Test hiện kiểm tra mapper/metadata SQLAlchemy, PostgreSQL DDL, bảng quan trọng, khóa ngoại, constraint, grain của fact table và an toàn cascade.

### Bước 7: Chạy FastAPI backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Mở các địa chỉ:

- Health check: [http://localhost:8000/health](http://localhost:8000/health)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

Kết quả health check mong đợi:

```json
{"status":"ok"}
```

### Bước 8: Cài và chạy frontend web

Mở terminal thứ hai tại thư mục gốc:

```bash
cd frontend
npm install
npm run dev
```

Mở [http://localhost:5173](http://localhost:5173). Vite lắng nghe trên `0.0.0.0:5173`, phù hợp cho thử nghiệm trong mạng nội bộ hoặc kiosk.

### Bước 9: Chạy chế độ kiosk Electron

Sau khi đã chạy `npm install`:

```bash
npm run electron:dev
```

Lệnh này khởi động Vite, chờ cổng 5173 sẵn sàng rồi mở Electron.

Build frontend web:

```bash
npm run build
npm run preview
```

Build bộ cài Electron:

```bash
npm run electron:build
```

Artifact được tạo trong `frontend/release/`. Quá trình build Electron có thể cần tải binary từ Internet.

## Quy trình chạy hằng ngày

Từ thư mục gốc:

```bash
docker compose up -d
```

Terminal backend:

```bash
cd backend
# Kích hoạt .venv
alembic upgrade head
uvicorn app.main:app --reload
```

Terminal frontend:

```bash
cd frontend
npm run dev
```

Dừng ứng dụng bằng `Ctrl+C`. Dừng hạ tầng:

```bash
docker compose down
```

Lệnh trên giữ dữ liệu trong Docker volumes. Chỉ dùng `docker compose down -v` khi chắc chắn muốn xóa toàn bộ dữ liệu PostgreSQL và Redis cục bộ.

## Database và analytics

Schema gồm 92 bảng, chia thành các miền:

- Identity, consent, FaceID và privacy
- Device, session và immutable interaction events
- Catalog chuẩn hóa, bản sách vật lý và ebook
- Search, AI request, RAG và recommendation attribution
- Mini-game, borrowing/return, notification và survey
- Research study, participant và A/B assignment
- Application telemetry và audit log
- Calendar/time dimensions, daily dashboard facts và book popularity
- AI model/prompt registry, staff/RBAC, academic/geographic analytics
- Dashboard configuration, KPI/alert governance và ML lineage

Các fact table dashboard là dữ liệu tổng hợp, không thay thế bảng nghiệp vụ. Chiến lược refresh, star schema và materialized views nằm trong `docs/dashboard/`.

Tài liệu quan trọng:

- [Thiết kế database](docs/database/DATABASE_DESIGN.md)
- [ERD](docs/database/ERD.md)
- [Data dictionary](docs/database/DATA_DICTIONARY.md)
- [40 research metrics](docs/database/RESEARCH_METRICS.md)
- [Kiến trúc dashboard](docs/dashboard/DASHBOARD_ARCHITECTURE.md)
- [KPI definitions](docs/dashboard/KPI_DEFINITIONS.md)
- [Data warehouse](docs/dashboard/DATA_WAREHOUSE.md)
- [Star schema](docs/dashboard/STAR_SCHEMA.md)
- [Materialized views](docs/dashboard/MATERIALIZED_VIEWS.md)

## Xử lý lỗi thường gặp

### Backend không kết nối được PostgreSQL

- Chạy `docker compose ps` và kiểm tra `postgres` healthy.
- Đối chiếu `DATABASE_URL` với tài khoản và cổng Docker Compose.
- Kiểm tra cổng 5432 có bị PostgreSQL khác chiếm dụng không.
- Xem `docker compose logs postgres`.

### Alembic không tìm thấy module `app`

Bạn đang chạy lệnh sai thư mục. Hãy `cd backend` trước khi chạy Alembic.

### PowerShell không cho kích hoạt virtual environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Frontend không mở được

- Kiểm tra `npm install` đã hoàn tất.
- Kiểm tra cổng 5173 chưa bị ứng dụng khác sử dụng.
- Chạy lại `npm run dev` và xem URL Vite in trong terminal.

### Tạo migration mới

Sau khi sửa model:

```bash
cd backend
alembic revision --autogenerate -m "mo ta thay doi"
alembic upgrade head
python -m pytest -q
```

Luôn đọc và review migration được sinh ra trước khi chạy trên database dùng chung.

## Những phần chưa triển khai

- CRUD/API nghiệp vụ hoàn chỉnh
- Authentication và phân quyền runtime
- Nhận diện hoặc phần cứng FaceID
- Gemini request thực tế và quản lý prompt runtime
- Redis cache/session client
- ETL jobs refresh fact table và materialized views
- Dashboard UI/BI deployment
- CI/CD và cấu hình production

Biometric template chỉ được thiết kế dưới dạng dữ liệu mã hóa hoặc secure external reference. Việc mã hóa, quản lý khóa, phân quyền, retention và audit phải được triển khai ở tầng security/service trước khi sử dụng FaceID thật.

## Nguyên tắc đóng góp

1. Không sửa migration đã chạy trên môi trường dùng chung; tạo revision mới.
2. Giữ event/audit tables theo hướng append-only.
3. Không lưu plaintext password, raw face image hoặc prompt nhạy cảm mặc định.
4. Thêm constraint/index có lý do và cập nhật tài liệu liên quan.
5. Chạy backend tests và frontend build trước khi gửi thay đổi.
6. Không commit `.env`, API key, database dump, virtual environment hoặc artifact build.
