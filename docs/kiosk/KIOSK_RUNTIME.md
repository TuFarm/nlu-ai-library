# Kiosk runtime

The React kiosk runs at `/kiosk/fullscreen`. It fills the viewport, uses large touch targets, minimal navigation and one state screen at a time.

Electron is already configured in `frontend/electron`. The secure preload exposes only the app version, context isolation stays enabled, and Electron initializes its in-memory route directly at the fullscreen kiosk. Development uses `npm run electron:dev`; `npm run electron:build` is reserved for a later packaging milestone.

Production deployment should decide whether FastAPI runs locally as a managed Windows service or on a protected server. Configure `VITE_API_BASE_URL` at build time. A Windows deployment can later add auto-start through an installer/startup task, process supervision, restricted exit controls and offline recovery.

Real camera/FaceID must add consent, liveness, encrypted template handling and retention policy. Do not store raw facial photos. Mock buttons remain until that integration is approved.

## Phase 3 media runtime

FastAPI now accepts validated image/audio multipart uploads, but Electron/browser still owns `getUserMedia`. Development files are written under `backend/storage/media` only for processing and deleted by default. Set `MEDIA_RETAIN_DEVELOPMENT_FILES=true` only for controlled debugging. `FACE_PROVIDER=local` is an isolated extension point and returns a clear unavailable error until a local engine is installed. See `FRONTEND_BACKEND_CONTRACT.md` for request order.
