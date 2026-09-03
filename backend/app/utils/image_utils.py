from pathlib import Path


def has_supported_image_signature(content: bytes, content_type: str) -> bool:
    signatures = {
        "image/jpeg": content.startswith(b"\xff\xd8\xff"),
        "image/png": content.startswith(b"\x89PNG\r\n\x1a\n"),
        "image/webp": content.startswith(b"RIFF") and content[8:12] == b"WEBP",
    }
    return signatures.get(content_type, False)


def filename_requests_unknown(path: Path) -> bool:
    """Test-only hint used by the dependency-free mock face provider."""
    return any(token in path.name.lower() for token in ("unknown", "stranger"))
