"""Validate image files before AI caption generation."""

from pathlib import Path
import argparse
import struct

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE_MB = 10


def validate_image(image_path):
    path = Path(image_path)

    if not path.is_file():
        raise ValueError("Image file does not exist")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError("Only JPG, JPEG, and PNG images are supported")

    size_mb = path.stat().st_size / (1024 * 1024)

    if size_mb == 0:
        raise ValueError("Image file is empty")

    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError("Image exceeds 10 MB limit")

    with path.open("rb") as image:
        header = image.read(24)

    if path.suffix.lower() == ".png":
        if not header.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Invalid PNG signature")

        if len(header) < 24 or header[12:16] != b"IHDR":
            raise ValueError("Invalid PNG header")

        width, height = struct.unpack(">II", header[16:24])

        if width == 0 or height == 0:
            raise ValueError("Invalid image dimensions")

        dimensions = f"{width}x{height}"
    else:
        if not header.startswith(b"\xff\xd8"):
            raise ValueError("Invalid JPEG signature")

        dimensions = "Not inspected"

    return {
        "filename": path.name,
        "size_mb": round(size_mb, 2),
        "format": path.suffix.lower(),
        "dimensions": dimensions,
        "status": "Basic validation passed",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate an image before caption generation"
    )
    parser.add_argument("image_path")
    args = parser.parse_args()

    try:
        result = validate_image(args.image_path)
        for key, value in result.items():
            print(f"{key}: {value}")
    except ValueError as error:
        parser.exit(1, f"Validation failed: {error}\n")
