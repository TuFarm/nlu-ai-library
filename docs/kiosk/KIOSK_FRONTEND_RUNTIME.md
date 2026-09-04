# Kiosk frontend runtime

Phase 4 created the browser/Electron runtime; Phase 5 extends it with face registration, optional local matching and turn-based voice/TTS. It remains separate from the staff-only Admin Web under `/admin`.

## State-driven flow

The kiosk is state-driven rather than menu-driven because a visitor should be guided through one obvious action at a time:

`IDLE → CAMERA_PERMISSION → CAMERA_READY → FACE_SCANNING → FACE_RECOGNIZED/FACE_UNKNOWN → FACE_REGISTER/WELCOME → VOICE_CHAT → BOOK_SUGGESTION/SURVEY → THANK_YOU → IDLE`

`useKioskFlow` owns the reducer, active session, recognized user, conversation, messages, device state, media state, errors and last activity timestamp. Backend `next_state` values are interpreted at the FaceID boundary. Admin components and navigation are never mounted inside `KioskLayout`.

## Runtime behavior

1. The visitor presses **Bắt đầu phiên thử nghiệm**. This user gesture starts a backend session and then requests camera permission.
2. `useCamera` attaches the `MediaStream` to a mirrored video preview. A frame is drawn to an in-memory canvas and encoded as JPEG.
3. The image blob, session ID and device code are posted to FaceID as multipart form data.
4. Recognized visitors see profile information; unknown visitors can retry or continue as a guest.
5. Welcome automatically advances to chat after 2.6 seconds. Chat accepts touch-friendly quick questions, keyboard text or Vietnamese browser speech recognition.
6. A voice transcript is first persisted at the voice endpoint. The AI endpoint then creates the response without duplicating that user message.
7. Categories, book suggestions and active survey questions are loaded from the Phase 3 database APIs.
8. Thank-you ends the session and returns to idle after five seconds. Any inactive non-busy state returns to idle after the configured timeout.

The idle timer pauses while speech recognition is listening and while a backend request is being processed. Pointer and keyboard activity refresh it.

## Development behavior

Development builds show a small panel for recognized face, unknown face, guest bypass and reset simulations. These controls are absent from production builds. Offline values are used only when `VITE_ENABLE_MOCK_FALLBACK=true`; otherwise a clear server connection error is shown.

Face matching can use the optional local provider and Gemini can use its real API. Mock fallbacks remain available. RAG and server-side production speech-to-text are not implemented; the browser owns STT/TTS for this turn-based demo.

## Electron readiness

The renderer uses standard browser APIs and has no Node.js access. Electron keeps context isolation enabled, grants only media-related runtime permissions, opens the fullscreen route through `MemoryRouter`, and is ready for later packaging/security hardening. Production work still needs OS permission validation, a trusted deployment origin, restricted navigation, device enrollment and biometric consent/retention policy.
