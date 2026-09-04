# Voice conversation runtime

Phase 5 implements a turn-based browser voice loop:

`AI greeting → LISTENING → USER_SPEAKING → TRANSCRIBING → PROCESSING_AI → AI_SPEAKING → LISTENING`

This is not low-latency, full-duplex streaming and should not be described as equivalent to ChatGPT Voice or Gemini Live. Each user turn completes speech recognition, one HTTP AI request and browser text-to-speech before the next listening turn begins.

## Speech recognition

`useSpeechRecognition` detects `SpeechRecognition` or `webkitSpeechRecognition`, configures `vi-VN`, provides interim/final transcript text and handles denied or unsupported browsers. The voice screen stops recognition before AI processing and never listens while synthesized speech is playing, which prevents the kiosk from hearing its own response.

The finalized transcript is persisted at `POST /api/v1/voice/browser-transcript`. The subsequent `/ai/answer` request sends `save_user_message=false` so the same voice turn is not stored twice.

## Text to speech

`useTextToSpeech` wraps `window.speechSynthesis`. It prefers an installed voice whose language starts with `vi` and otherwise uses the browser default with a visible notice. Welcome and voice-chat greeting messages are spoken. Each AI answer is displayed, spoken, and followed by automatic listening when voice recognition remains available.

`speak(text, options)` resolves when speech ends or fails; `stop()` cancels current speech. The hook exposes speaking, support, error and Vietnamese-voice availability state.

## Fallbacks and controls

Keyboard input and quick questions always remain available. Denying microphone permission changes the screen to `VOICE_ERROR` without ending the session. Users can manually restart speech, type, open suggestions/survey or end the session. Development mode can stop voice and test TTS.

Browser Web Speech availability varies by browser and may depend on an online vendor service. For an offline or controlled production kiosk, replace it with a deliberately selected onsite/cloud STT provider.
