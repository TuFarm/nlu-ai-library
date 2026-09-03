# Kiosk flow

The kiosk behaves like an appliance, not a website. There is no feature sidebar and the user sees only the current step.

```text
IDLE → PRESENCE_DETECTED → FACE_SCANNING
                           ├─ SUCCESS → FACE_RECOGNIZED → WELCOME → AI_CHAT
                           ├─ UNKNOWN/LOW/TIMEOUT → FACE_UNKNOWN → retry or guest → AI_CHAT
                           └─ ERROR → ERROR
AI_CHAT ↔ BOOK_SUGGESTION → SURVEY → THANK_YOU → IDLE
```

Presence and face input are buttons in mock mode. A recognized identity includes student profile data; unknown visitors remain anonymous. Pointer or keyboard interaction refreshes the idle timer. Inactivity resets identity, session and conversation state. Thank-you automatically resets after seven seconds.

Future mode replaces presence/face buttons with hardware events, chat mock with Gemini plus grounded RAG, and in-memory transitions with persisted session events. The public state names should remain stable.
