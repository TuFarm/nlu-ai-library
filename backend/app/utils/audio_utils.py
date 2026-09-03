from pathlib import Path


def has_supported_audio_signature(content: bytes, content_type: str) -> bool:
    checks = {
        "audio/wav": content.startswith(b"RIFF") and content[8:12] == b"WAVE",
        "audio/x-wav": content.startswith(b"RIFF") and content[8:12] == b"WAVE",
        "audio/webm": content.startswith(b"\x1aE\xdf\xa3"),
        "audio/mpeg": content.startswith(b"ID3") or content.startswith(b"\xff"),
        "audio/mp4": content[4:8] == b"ftyp",
        "audio/ogg": content.startswith(b"OggS"),
    }
    return checks.get(content_type, False)


def audio_extension(path: Path) -> str:
    return path.suffix.lower().lstrip(".")
