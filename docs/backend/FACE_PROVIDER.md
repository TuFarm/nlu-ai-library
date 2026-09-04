# Face provider

## Mock mode

`FACE_PROVIDER=mock` requires no native packages and keeps CI, classroom setup and non-biometric UI development reliable. It does not perform real recognition.

## Optional local mode

Use Python 3.12. From `backend`:

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-face-local.txt
```

Then set:

```dotenv
FACE_PROVIDER=local
FACE_CONFIDENCE_THRESHOLD=0.75
```

The adapter lazily imports `face_recognition`. Therefore a missing native dependency never prevents the FastAPI app from importing; only local enrollment/verification returns `FACE_PROVIDER_UNAVAILABLE`.

The provider uses the CPU HOG detector and 128-dimensional face encodings. Enrollment requires exactly one detected face. Verification compares the probe against all active profiles with Euclidean distance and reports `confidence = max(0, 1 - distance)`. The configured threshold is strict; tune it only with representative, consented validation data and record false accepts/rejects.

## Windows notes

`face_recognition` depends on `dlib`. Installation may require Microsoft C++ Build Tools and CMake, and wheel availability varies by Python/Windows version. Keep the optional file out of the base requirements. If installation is impractical, use mock mode or package a vetted native wheel/provider separately; do not weaken startup reliability.

## Storage and security

Local embeddings are JSON-serialized bytes stored in `face_profiles.face_template_encrypted`. They are not raw images, but they are still sensitive biometric identifiers and are not actually encrypted by this development implementation. Temporary images are excluded by `.gitignore` and deleted after processing by default.

Production must add real authenticated encryption, managed keys, liveness/anti-spoofing, consent evidence, RBAC, audit access, retention/deletion workflows, backup policy, legal review and ongoing demographic performance evaluation.
