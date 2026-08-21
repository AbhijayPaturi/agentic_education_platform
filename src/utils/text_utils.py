"""Pure text helpers shared across the codebase.

This module intentionally has no internal dependencies so it can be imported
from anywhere (including ``config``) without risking circular imports.
"""

from __future__ import annotations

_ALLOWED_EXTRA_CHARS = (" ", "_", "-")


def sanitize_filename(name: str) -> str:
    """Convert an arbitrary string into a filesystem-safe path component.

    Alphanumeric characters and ``space``/``_``/``-`` are preserved; every
    other character (including path separators such as ``/`` and ``\\``) is
    replaced with an underscore. Spaces are then collapsed to underscores so
    the result is safe to use as a single directory or file name.

    Args:
        name: The raw string to sanitize (e.g. a topic or career goal).

    Returns:
        A sanitized string safe to use as a single path segment. Falls back to
        ``"untitled"`` when the input reduces to an empty string.
    """
    sanitized = "".join(
        c if c.isalnum() or c in _ALLOWED_EXTRA_CHARS else "_" for c in name
    ).strip()
    sanitized = sanitized.replace(" ", "_")
    return sanitized or "untitled"
