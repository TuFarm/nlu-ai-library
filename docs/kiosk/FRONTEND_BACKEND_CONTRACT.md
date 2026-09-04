# Frontend–backend kiosk contract

The backend cannot open browser/Electron hardware. The frontend owns camera, microphone and browser speech recognition, then sends media or transcript data to FastAPI. All API responses use `{ success, message, data, error? }`.

`VITE_API_BASE_URL` is the server origin (`http://localhost:8000` by default). The client appends `/api/v1`; it also accepts a configured URL that already ends in `/api/v1`.

| Purpose | Request | Important response |
|---|---|---|
| Start session | `POST /api/v1/kiosk/sessions/start` with device code | session ID, device ID, next state |
| Log event | `POST /api/v1/kiosk/sessions/{id}/events` | event ID |
| End session | `POST /api/v1/kiosk/sessions/{id}/end` | `next_state: IDLE` |
| Verify face | `POST /api/v1/face/verify` multipart | result, user, confidence, next state |
| Register face | `POST /api/v1/face/enroll` multipart image and user fields | profile, user, `WELCOME` |
| Start conversation | `POST /api/v1/conversations/start` | conversation ID |
| Read messages | `GET /api/v1/conversations/{id}/messages` | normalized message list |
| Browser voice | `POST /api/v1/voice/browser-transcript` | stored message ID |
| AI answer | `POST /api/v1/ai/answer` | answer, provider, warning, `AI_VOICE_CHAT` |
| Book categories | `GET /api/v1/book-categories` | category records |
| Suggested books | `GET /api/v1/suggested-books?category_id=...` | simple book records |
| Active survey | `GET /api/v1/surveys/active` | survey or `null` |
| Submit survey | `POST /api/v1/surveys/{id}/responses` | response ID/count |
| Admin data | `/api/v1/admin/dashboard/mock` and `/api/v1/admin/status` | admin data |

For text, `/ai/answer` stores the user message. For voice, `/voice/browser-transcript` stores it first and the AI request sends `save_user_message:false`, avoiding duplicate conversation history.

Images are JPEG blobs created from the current preview frame. The development backend validates MIME type and its configured 5 MB limit, then deletes raw verification/enrollment media unless retention is explicitly enabled. Browser STT plus browser TTS form the Phase 5 turn-based voice path; audio upload/server STT remains optional.

Offline fallback is never implicit. It is allowed only when `VITE_ENABLE_MOCK_FALLBACK=true`, and the kiosk displays a notice when it uses an offline AI response or sample book/survey data.
