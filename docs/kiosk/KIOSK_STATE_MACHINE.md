# Kiosk state machine

`useKioskFlow` uses `useReducer`; components render state and invoke domain actions without owning session transitions.

| State | Entry | Exit |
|---|---|---|
| `IDLE` | Initial/reset state; media stopped | `START_SESSION` |
| `CAMERA_PERMISSION` | Session exists; camera is requesting, denied or retryable | granted → `CAMERA_READY`; guest → `WELCOME` |
| `CAMERA_READY` | Preview is live | automatic → `FACE_SCANNING` |
| `FACE_SCANNING` | Capture and multipart verification | success/unknown/failure |
| `FACE_RECOGNIZED` | User and confidence stored | automatic → `WELCOME` |
| `FACE_UNKNOWN` | Retry, guest and disabled enrollment choice | scan or `WELCOME` |
| `WELCOME` | Personalized or guest greeting | button/timer → `AI_CHAT` |
| `AI_CHAT` | Conversation and messages active | books, survey or error |
| `BOOK_SUGGESTION` | Database categories/books | chat or survey |
| `SURVEY` | Active database survey | `THANK_YOU` |
| `THANK_YOU` | Session completion notice | button/5 s → `IDLE` |
| `ERROR` | Recoverable friendly error | reset to idle |

Reducer state also stores the session, device, user, conversation, camera/microphone status, last face result, transcript, messages, AI response, selected category, suggested books, survey, error, busy state and `lastActivityAt`.

The public reducer actions include all Phase 4 domain actions: `START_SESSION`, camera grant/deny, `START_FACE_SCAN`, face success/unknown/failure, `CONTINUE_AS_GUEST`, `START_CONVERSATION`, user/AI messages, books, survey submit, session end, reset and error. Small `SET_*`, `TOUCH` and `TRANSITION` actions support browser device state and screen orchestration.

The inactivity deadline is `lastActivityAt + VITE_KIOSK_IDLE_TIMEOUT_SECONDS`. Timeout sends `exit_reason=TIMEOUT`, stops media when idle renders, and clears all user/session data. Processing and active listening suspend the countdown.
