# Gemini integration

Set:

```dotenv
AI_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-3.8-flash
GEMINI_TIMEOUT_SECONDS=20
```

Do not commit the real key. Restart FastAPI after changing environment values.

`AIService` uses the Gemini `generateContent` REST endpoint through the already-required `httpx` package. It sends a Vietnamese library-receptionist system instruction, up to ten recent user/assistant messages and the current turn. The prompt explicitly forbids invented official policies, hours, WiFi credentials and locations because RAG is not connected.

The model is configurable because Gemini names and lifecycle change. Check the official Gemini model documentation before deployment. The default selected during Phase 5 is `gemini-3.8-flash`.

## Failure behavior

If `AI_PROVIDER` is not `gemini`, the mock provider is used. If the key is empty, the network call fails, Gemini returns invalid data, or the request times out:

- the service returns a concise safe mock response;
- the endpoint still returns a successful envelope so the kiosk voice loop continues;
- a missing key is saved as `fallback`; an attempted provider call that errors is saved as `failed`;
- the response provider is `mock` and includes a warning;
- the `AI_ANSWERED` interaction is recorded with `success=false`.

Successful Gemini calls store user and assistant conversation messages, `ai_requests` with `completed`, `ai_responses` and interaction events. Responses remain `grounded=false` until Phase 6 adds document retrieval.

This is turn-based text generation. Browser STT produces text before Gemini is called, and browser TTS speaks the returned text afterward. Gemini Live streaming is not used.
