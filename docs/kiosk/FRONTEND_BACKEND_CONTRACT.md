# Frontend–backend camera and microphone contract

The backend cannot open a browser/Electron camera or microphone. The renderer owns permission prompts and media capture through `navigator.mediaDevices.getUserMedia`.

## Camera

1. Request video permission and render a local preview.
2. Draw one frame to a canvas and encode JPEG/PNG/WebP.
3. Send `multipart/form-data` with `image_file`, optional `session_id`, and optional `device_code` to `POST /api/v1/face/verify`.
4. On `SUCCESS`/`WELCOME`, store returned user in kiosk flow. On `UNKNOWN_FACE`/`FACE_UNKNOWN`, show retry/guest actions. Provider errors go to the error screen.
5. Enrollment sends `user_id`, optional session/device IDs and `image_file` to `/api/v1/face/enroll` only after explicit consent.

## Microphone

Record WebM/WAV/MP3/M4A/OGG and submit `audio_file` plus optional session/conversation IDs to `/api/v1/voice/transcribe`. Alternatively, use browser Web Speech API and send JSON `{ session_id, conversation_id, transcript, confidence_score }` to `/api/v1/voice/browser-transcript`.

After transcript persistence, send `{ conversation_id, session_id, message_text }` to `/api/v1/ai/answer`, display `answer`, then remain in `AI_CHAT`. Submit the active survey at session end.

Image limit is 5 MB and audio limit is 15 MB by default. The development backend validates MIME types. Raw media is deleted after processing unless `MEDIA_RETAIN_DEVELOPMENT_FILES=true`; production must use consent, encryption and retention controls.
