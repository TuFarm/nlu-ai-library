# Kiosk flow

```text
IDLE → CAMERA_PERMISSION → CAMERA_READY → FACE_SCANNING
  ├─ SUCCESS → FACE_RECOGNIZED → WELCOME → VOICE_CHAT
  └─ UNKNOWN / LOW_CONFIDENCE
       → FACE_UNKNOWN
          ├─ register → FACE_REGISTER → FACE_RECOGNIZED
          ├─ retry → FACE_SCANNING
          └─ guest → WELCOME → VOICE_CHAT

VOICE_CHAT
  → LISTENING → USER_SPEAKING → PROCESSING_AI
  → AI_SPEAKING → LISTENING
  ↔ BOOK_SUGGESTION
  → SURVEY → THANK_YOU → IDLE
```

Camera, microphone and TTS are stopped during session reset. Voice is turn-based and microphone recognition stays off while the assistant is speaking.
