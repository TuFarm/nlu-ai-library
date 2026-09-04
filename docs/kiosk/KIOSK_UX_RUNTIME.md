# Production kiosk UX runtime

Phase 5.5 treats the fullscreen route as an always-running receptionist, not a navigable website. The interface owns one continuous conversation, keeps controls exceptional, uses large touch targets, and explains every wait with motion and plain Vietnamese copy.

## Why the flow is paced

- **Presence detection** prevents an empty lobby, passers-by, or camera startup from creating sessions and FaceID requests. A person must remain visible for about 1.2 seconds.
- **Camera preparation** gives exposure and focus one second to settle before quality checks begin.
- **Face stabilization** avoids repeated or blurred captures. A native `FaceDetector` is used when Chromium exposes it; otherwise a low-resolution motion/contrast heuristic provides a development fallback.
- **Countdown** gives the visitor a predictable moment to become still. It uses 3–2–1 at 500 ms per number and captures exactly one frame.
- **Verification** remains visible for at least one second even when the API is faster, so success or an unknown result has an understandable cause.
- **Welcome** stays visible for three seconds so identity and student information can be read from 1.5–2 metres away.
- **Voice handoff** waits for speech synthesis to finish and then holds 500 ms of silence before enabling recognition. This prevents the microphone from transcribing the assistant.

## Runtime guarantees

- Camera requests are limited to 30 fps and sampled at a lower rate for presence/stability.
- Only one FaceID verification may be active; a failed attempt has a two-second cooldown.
- Speech recognition has an activation lock. TTS cancels and resolves an earlier utterance before starting another.
- Camera frames stay in memory and only the selected JPEG is sent through the existing FaceID API.
- A session timeout never interrupts active processing or listening.
- `prefers-reduced-motion` keeps the experience usable for motion-sensitive visitors.

## Interaction model

Idle, presence, camera preparation, stabilization, countdown, capture, verification, success and voice startup are automatic. Buttons remain only for exceptional choices: unknown visitor actions, registration navigation, survey and ending the session. Keyboard input appears only when browser speech recognition is unavailable.

## Manual acceptance test

1. Open the fullscreen kiosk and confirm there is no start button. With nobody in view, it must remain idle.
2. Step into view and move naturally. After confirmed presence, verify the greeting, one-second camera preparation and stabilization guidance.
3. Move your head during stabilization; countdown must wait. Hold still and confirm 3–2–1 followed by one capture and one verification request.
4. Test a known profile. Confirm the success animation, three-second identity card, spoken personalized greeting and microphone activation only after speech plus 500 ms.
5. Test an unknown profile. Confirm it is presented as a friendly choice, not an error, and that retry/register/guest actions work.
6. Complete registration. Confirm information is split across short steps and capture → processing → success is visible.
7. During voice chat, ask two questions. Confirm listening stops while processing/TTS and resumes automatically without duplicated microphone prompts.
8. Finish through survey or the Finish action. Confirm a three-second goodbye and smooth return to idle with camera observation restored.
9. Leave during a non-processing state and wait for the configured inactivity timeout. Confirm the session ends and returns to idle.
10. Disconnect camera/backend and confirm the kiosk shows a recoverable permission/error choice rather than browser navigation or a blank screen.
