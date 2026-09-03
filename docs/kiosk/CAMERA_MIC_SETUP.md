# Camera and microphone setup

## Browser test

Run the backend and frontend, open `http://localhost:5173/kiosk/fullscreen`, then press **Bắt đầu phiên thử nghiệm**. Camera access is deliberately requested only after that user action.

When prompted:

- allow camera access to see the live preview and run face verification;
- allow microphone access after pressing **Nhấn để nói** in chat;
- speak Vietnamese because recognition uses `vi-VN`.

`localhost` is treated as a secure browser context. A kiosk served from another machine/IP normally needs HTTPS for `getUserMedia`. Close other programs holding the webcam or microphone if the browser reports that the device is unavailable.

## Camera path

`useCamera.requestCamera()` calls `navigator.mediaDevices.getUserMedia({ video, audio: false })`. `CameraPreview` displays the stream. `captureFrame()` draws the current video pixels into a temporary canvas and creates an `image/jpeg` blob at quality 0.88. The blob never enters React state and is sent immediately as:

- `session_id`
- `device_code`
- `image_file`

to `POST /api/v1/face/verify`. Stopping or resetting the session stops every media track.

If permission is denied, use the browser site controls to change Camera to Allow and retry. The visitor can always continue as a guest.

## Speech path

`useSpeechRecognition` detects `SpeechRecognition` or `webkitSpeechRecognition`, uses Vietnamese (`vi-VN`), displays interim words, and submits only the final transcript. The transcript and confidence are posted to `/api/v1/voice/browser-transcript`, followed by `/api/v1/ai/answer`.

Web Speech availability depends on the browser build and, in some browsers, an online recognition service. When unsupported or denied, the large text field remains fully usable. The UI never blocks the kiosk on microphone availability.

## Electron test

From `frontend`, run `npm run electron:dev`. The Electron main process allows camera/microphone media permission requests and loads `/kiosk/fullscreen`. Validate Windows privacy settings for both Camera and Microphone if no OS-level prompt appears.

## Troubleshooting

- No preview: reload, check the browser site permission icon, then close video-call applications.
- Permission denied persists: clear the site permission and request it again from the start screen.
- Speech unsupported: use Chrome/Edge for the browser test or use text input.
- Backend error after capture: confirm FastAPI is listening on port 8000, the database is seeded, and `VITE_API_BASE_URL` is correct.
- No recognized user: Phase 3 uses a mock face provider but still needs the seeded active face profile. Use guest flow or the development simulation panel.
