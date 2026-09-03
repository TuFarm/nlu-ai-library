# Frontend structure

The frontend contains two deliberately separate products.

## Admin Web

`AdminLayout` owns the staff sidebar and topbar. Routes are `/admin/dashboard`, `/admin/knowledge`, `/admin/conversations`, `/admin/users`, `/admin/surveys`, `/admin/reports`, and `/admin/status`; `/admin` redirects to the dashboard. Existing cards, tables, badges and under-development patterns remain admin-only.

## Kiosk App

`KioskLayout` is fullscreen and has no sidebar. `/kiosk` redirects to `/kiosk/fullscreen`. `KioskApp` renders one state screen at a time through `useKioskFlow`: idle, presence detected, face scanning, recognized/unknown, welcome, chat, books, survey, thank-you or error. Pointer/keyboard activity refreshes the configurable inactivity timer (`VITE_KIOSK_TIMEOUT_SECONDS`, default 120 seconds).

Electron is detected through the secure preload bridge. Web uses `BrowserRouter`; Electron uses `MemoryRouter` initialized directly at `/kiosk/fullscreen`, avoiding file-URL routing issues.

`apiClient` calls backend mocks. Chat, identity, sessions and surveys continue with local mock values when the backend is offline. No camera, Gemini, RAG or persistent upload is active.
