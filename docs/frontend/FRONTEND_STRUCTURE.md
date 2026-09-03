# Frontend structure

The React frontend contains two deliberately separate products.

## Admin Web

`AdminLayout` owns the staff sidebar/topbar and routes `/admin/dashboard`, `/admin/knowledge`, `/admin/conversations`, `/admin/users`, `/admin/surveys`, `/admin/reports`, and `/admin/status`. Phase 4 did not replace its existing mock/placeholder management data.

## Kiosk App

`KioskLayout` is fullscreen and never renders the admin sidebar. `/kiosk` redirects to `/kiosk/fullscreen`. Main modules:

- `pages/kiosk/KioskApp.tsx`: screen composition, camera lifecycle and development controls.
- `hooks/useKioskFlow.ts`: reducer, session/conversation APIs, transitions and idle reset.
- `hooks/useCamera.ts`: permission request, stream cleanup and JPEG frame capture.
- `hooks/useSpeechRecognition.ts`: Vietnamese Web Speech lifecycle and transcript results.
- `components/kiosk/CameraPreview.tsx`: reusable video, scan overlay and device state.
- `components/kiosk/VoiceInputButton.tsx`: accessible idle/listening/processing control.
- `services/apiClient.ts`: response-envelope handling and typed domain clients.
- `pages/kiosk/*Screen.tsx`: focused welcome, chat, books, survey and completion views.

Kiosk session state is centralized. Screen-local state is limited to transient form/UI values such as the chat input, loaded category, and survey answers.

The API client keeps JSON and multipart behavior in one place. It does not set `Content-Type` for `FormData`, allowing the browser to create the multipart boundary.

## Environment

```dotenv
VITE_API_BASE_URL=http://localhost:8000
VITE_KIOSK_DEVICE_CODE=KIOSK_DEV_01
VITE_ENABLE_MOCK_FALLBACK=true
VITE_KIOSK_IDLE_TIMEOUT_SECONDS=60
```

Use `false` for mock fallback when validating backend failure behavior. Vite development mode alone controls visibility of FaceID simulation/reset tools.

Web builds use `BrowserRouter`. Electron uses its preload marker and `MemoryRouter` initialized at `/kiosk/fullscreen`, which works with the packaged `file:` entry point.
