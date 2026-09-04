# FaceID runtime

## Enrollment

The unknown-face screen offers registration, retry and guest access. Registration collects a required full name plus optional student code, email, phone, faculty, major and admission year. The current camera frame is encoded as JPEG and sent as multipart data to `POST /api/v1/face/enroll`.

The endpoint supports an existing `user_id` or create/update-by-student-code/email. It validates the session and image, creates or updates `users`, creates or updates an active `face_profiles` row, associates the session with the user, and records `FACE_ENROLLED`. A successful response contains the user and `next_state=WELCOME`.

In local mode, exactly one face must be visible. The 128-dimensional encoding is serialized into `face_template_encrypted`. Despite that historical column name, the development implementation stores serialized bytes, not cryptographically encrypted data. Raw images are temporary and deleted after processing unless development retention is explicitly enabled.

## Verification

`POST /api/v1/face/verify` receives `session_id`, `device_code` and `image_file`. Local mode:

1. detects exactly one face with the HOG detector;
2. extracts a 128-dimensional encoding;
3. loads all active face profile embeddings;
4. calculates face distances;
5. selects the lowest distance;
6. converts it to `confidence = clamp(1 - distance, 0, 1)`;
7. returns `SUCCESS` only at or above `FACE_CONFIDENCE_THRESHOLD`.

Near-threshold matches return `LOW_CONFIDENCE`; profiles without a usable local embedding are ignored. Unknown attempts intentionally keep `user_id=null` because no identity has been established. Every processed attempt writes `face_authentication_logs`, and recognized sessions update `user_sessions.user_id` and `identified`.

## Provider modes

- `FACE_PROVIDER=mock`: dependency-free deterministic development provider.
- `FACE_PROVIDER=local`: optional `face_recognition` adapter.

If the optional library is missing, the API returns HTTP 503 with `FACE_PROVIDER_UNAVAILABLE` and guidance to install it or switch to mock mode. The app itself still imports and boots.

## Privacy warning

This is a development demo, not production biometric security. Production requires explicit informed consent, template encryption with managed keys, strict access control, audit trails, retention limits, revocation/deletion workflows, incident response, regional legal review, liveness/anti-spoofing, bias testing and documented alternatives for users who decline FaceID. Never commit captured images or biometric templates.
