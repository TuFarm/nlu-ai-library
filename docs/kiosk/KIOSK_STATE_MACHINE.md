# Kiosk state machine

`useKioskFlow` owns the session-level reducer. `KioskVoiceChatScreen` owns the faster voice sub-state because speech recognition and synthesis are browser lifecycles, not backend navigation states.

## Session states

| State | Purpose | Main transition |
|---|---|---|
| `IDLE` | No active visitor/session media | start → `CAMERA_PERMISSION` |
| `CAMERA_PERMISSION` | Request/retry camera or guest | grant → `CAMERA_READY` |
| `CAMERA_READY` | Live preview prepared | automatic → `FACE_SCANNING` |
| `FACE_SCANNING` | Capture and verify one frame | recognized/unknown |
| `FACE_RECOGNIZED` | Short success animation | automatic → `WELCOME` |
| `FACE_UNKNOWN` | Register, retry or guest | selected path |
| `FACE_REGISTER` | Profile form and face enrollment | success → `FACE_RECOGNIZED` |
| `WELCOME` | Smile, user card and spoken greeting | automatic → `VOICE_CHAT` |
| `VOICE_CHAT` | Conversation and browser voice loop | books/survey/end |
| `BOOK_SUGGESTION` | Simple topic suggestions | back → `VOICE_CHAT` |
| `SURVEY` | Active survey | submit → `THANK_YOU` |
| `THANK_YOU` | Completion notice | five seconds → `IDLE` |
| `ERROR` | Recoverable runtime failure | reset |

`AI_CHAT` remains accepted as a compatibility alias and renders the voice chat screen.

## Voice sub-states

`VOICE_IDLE`, `LISTENING`, `USER_SPEAKING`, `TRANSCRIBING`, `PROCESSING_AI`, `AI_SPEAKING` and `VOICE_ERROR` control animation, labels, microphone behavior and automatic restart.

The inactivity timer defaults to 90 seconds. It pauses during backend processing, microphone listening and TTS/voice processing. Reset ends the backend session, stops camera/microphone/speech synthesis and clears identity/conversation state.
