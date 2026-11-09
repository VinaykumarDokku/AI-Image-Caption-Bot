"""Utilities for processing generated image captions."""

import re


def clean_caption(caption):
    """Normalize whitespace in a generated caption."""
    if not isinstance(caption, str):
        raise TypeError("Caption must be a string")

    return re.sub(r"\s+", " ", caption).strip()


def word_count(caption):
    """Count words in a cleaned caption."""
    cleaned = clean_caption(caption)
    return len(cleaned.split()) if cleaned else 0
