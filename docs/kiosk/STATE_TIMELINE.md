# Kiosk state timeline

## Main path

| State | Trigger | Minimum presentation | Next state |
| --- | --- | ---: | --- |
| `IDLE` | Kiosk ready; camera observes silently | Unlimited | `PRESENCE_DETECTED` after confirmed presence |
| `PRESENCE_DETECTED` | Person remains present | 1200 ms | `CAMERA_PREPARING` |
| `CAMERA_PREPARING` | Session created | 1000 ms | `FACE_STABILIZING` |
| `FACE_STABILIZING` | Face/scene motion is below threshold | 1200 ms stable | `COUNTDOWN` |
| `COUNTDOWN` | Stable face | 3 × 500 ms | `FACE_CAPTURE` |
| `FACE_CAPTURE` | Countdown completes | One frame | `VERIFYING` |
| `VERIFYING` | API request active | 1000 ms | `FACE_SUCCESS` or `UNKNOWN_FACE` |
| `FACE_SUCCESS` | Known profile returned | 800 ms | `GREETING` |
| `GREETING` | Identity card visible | 3000 ms + TTS | `VOICE_GREETING` |
| `VOICE_GREETING` | Conversation created | TTS duration + 500 ms | `VOICE_LISTENING` |
| `VOICE_LISTENING` / `LISTENING` | Micro active | Until final transcript | `USER_SPEAKING` then `PROCESSING` |
| `PROCESSING` | AI request active | API duration | `AI_SPEAKING` |
| `AI_SPEAKING` | Answer available | TTS duration + 500 ms | `LISTENING` |
| `SURVEY` | Visitor chooses survey | User controlled | `THANK_YOU` |
| `THANK_YOU` | Session finishes | 3000 ms | `RETURN_IDLE` |
| `RETURN_IDLE` | Goodbye completes | 500 ms fade | `IDLE` |

## Unknown and registration branch

`UNKNOWN_FACE` offers **Đăng ký khuôn mặt**, **Thử lại**, and **Tiếp tục với tư cách khách**. Registration is a wizard: information (split into identity and academic details), capture, processing, and success. `REGISTER_SUCCESS` remains visible for 2200 ms before joining `GREETING`.

## Timing ownership

All timing lives in `frontend/src/config/kioskRuntime.ts`. Components do not define independent production delays. This keeps Electron, browser development and automated tests aligned.

