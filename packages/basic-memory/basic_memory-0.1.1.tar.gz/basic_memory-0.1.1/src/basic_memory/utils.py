"""Utility functions for basic-memory."""
import os
import re
import unicodedata
from pathlib import Path

from unidecode import unidecode


def sanitize_name(name: str) -> str:
    """
    Sanitize a name for filesystem use:
    - Convert to lowercase
    - Replace spaces/punctuation with underscores
    - Remove emojis and other special characters
    - Collapse multiple underscores
    - Trim leading/trailing underscores
    """
    # Normalize unicode to compose characters where possible
    name = unicodedata.normalize("NFKD", name)
    # Remove emojis and other special characters, keep only letters, numbers, spaces
    name = "".join(c for c in name if c.isalnum() or c.isspace())
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    # Remove newline
    name = name.replace("\n", "")
    # Convert to lowercase
    name = name.lower()
    # Collapse multiple underscores and trim
    name = re.sub(r"_+", "_", name).strip("_")

    return name


def generate_permalink(file_path: Path | str) -> str:
    """Generate a stable permalink from a file path.

    Args:
        file_path: Original file path

    Returns:
        Normalized permalink that matches validation rules. Converts spaces and underscores
        to hyphens for consistency.

    Examples:
        >>> generate_permalink("docs/My Feature.md")
        'docs/my-feature'
        >>> generate_permalink("specs/API (v2).md")
        'specs/api-v2'
        >>> generate_permalink("design/unified_model_refactor.md")
        'design/unified-model-refactor'
    """
    # Remove extension
    base = os.path.splitext(file_path)[0]

    # Transliterate unicode to ascii
    ascii_text = unidecode(base)

    # Insert dash between camelCase
    ascii_text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", ascii_text)

    # Convert to lowercase
    lower_text = ascii_text.lower()

    # replace underscores with hyphens
    text_with_hyphens = lower_text.replace('_', '-')

    # Replace remaining invalid chars with hyphens
    clean_text = re.sub(r'[^a-z0-9/\-]', '-', text_with_hyphens)

    # Collapse multiple hyphens
    clean_text = re.sub(r'-+', '-', clean_text)

    # Clean each path segment
    segments = clean_text.split('/')
    clean_segments = [s.strip('-') for s in segments]

    return '/'.join(clean_segments)
