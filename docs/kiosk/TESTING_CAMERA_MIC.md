# Laptop camera and microphone testing

Use Chrome or Edge on `http://localhost`, or `npm run electron:dev`. Start PostgreSQL, apply migrations, seed data, run FastAPI, then run Vite.

## Manual test 1 — enrollment and verification

1. Open `http://localhost:5173/kiosk/fullscreen`.
2. Start the session and allow camera access.
3. Scan an unknown face and confirm registration/retry/guest choices.
4. Choose **Đăng ký ngay**, enter user information and select **Chụp và đăng ký**.
5. Confirm the success/smile welcome appears.
6. Start a fresh session and scan the same face.
7. Confirm the user is recognized and the spoken greeting opens voice chat.

For real matching, use `FACE_PROVIDER=local` and install the optional dependency. Mock mode validates the flow but is not biometric matching.

## Manual test 2 — voice round trip

1. Allow microphone access when voice chat opens.
2. Ask: “Thư viện mở cửa lúc mấy giờ?”
3. Confirm interim/final transcript text appears.
4. Confirm the AI response appears and is read aloud.
5. Confirm the status returns to “Tôi đang nghe...” only after speech ends.
6. Confirm the kiosk does not transcribe its own synthesized response.

## Manual test 3 — permission and capability fallback

1. Deny microphone permission.
2. Confirm a Vietnamese permission message appears.
3. Enter a question with the keyboard and confirm the response still works.
4. Repeat with camera denied and confirm guest access remains available.

## Manual test 4 — Gemini fallback

1. Set `AI_PROVIDER=gemini` and leave `GEMINI_API_KEY` empty.
2. Restart FastAPI and send a text or voice question.
3. Confirm a friendly mock response is returned and the kiosk continues.
4. Inspect `ai_requests.status` and confirm it is `fallback`.

## Troubleshooting

- Camera/microphone access outside localhost generally requires HTTPS.
- Close video conferencing software if a device is busy.
- Windows privacy settings must allow the browser or Electron camera/microphone access.
- If local FaceID returns 503, install `backend/requirements-face-local.txt` or use mock mode.
- If no Vietnamese TTS voice exists, install a Vietnamese OS voice; the browser default still speaks.
- Hardware permissions cannot be reliably validated by unit tests and must be checked on the target kiosk.
