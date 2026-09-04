# Electron readiness

The kiosk experience no longer depends on browser navigation or page changes. Electron can keep loading `/kiosk/fullscreen` through the existing memory router.

## Ready now

- Fullscreen single-flow experience with no sidebar or back navigation.
- Automatic camera startup, presence observation and one-frame FaceID capture.
- Camera constraints capped at 30 fps.
- Touch targets of at least 48 px, high contrast and large distance-readable typography.
- Mouse, touch and keyboard activity reset the inactivity timer.
- Microphone starts only after TTS completion plus a 500 ms guard.
- Duplicate FaceID, microphone and TTS work is guarded.
- Camera is released during greeting/voice and reopened on return to idle.
- Friendly permission fallback for browser development.
- Developer controls remain development-only.

## Packaging checklist

- [ ] Configure Electron media permission handlers for the production origin.
- [ ] Verify the selected Windows camera and microphone after reboot.
- [ ] Install a Vietnamese Windows TTS voice and confirm the chosen voice.
- [ ] Configure Windows auto-start and disable sleep, notifications and screen savers.
- [ ] Hide cursor after inactivity and provide an administrator-only exit gesture.
- [ ] Run the backend as a supervised local service or configure a protected remote API.
- [ ] Set the production `VITE_API_BASE_URL` before building Electron.
- [ ] Test offline, backend restart and camera disconnect recovery.
- [ ] Calibrate presence/motion thresholds at the physical kiosk location.
- [ ] Complete biometric consent, retention, encryption and liveness controls before production use.

Browser presence fallback uses visual motion because the Shape Detection API is not guaranteed. For a fixed production device, validate native `FaceDetector` availability or add the selected on-device presence model in Phase 6 without changing the UX state machine.

