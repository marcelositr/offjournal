# core/utils.py

"""
Utility functions for offjournal.

Provides generic helper functions to support other modules.

Author: Marcelo (o Jedi dos Utils)
"""

import os
from pathlib import Path
from datetime import datetime

def ensure_dir(path: str) -> None:
    """
    Verifies if a directory exists, and creates it if it does not.

    Args:
        path (str): Directory path to check/create.
    """
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

def read_file(filepath: str) -> str:
    """
    Reads the content of a text file.

    Args:
        filepath (str): Path to the file.

    Returns:
        str: Content of the file.
    """
    p = Path(filepath)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filepath: str, content: str) -> None:
    """
    Writes content to a text file, overwriting if it exists.

    Args:
        filepath (str): Path to the file.
        content (str): Content to write.
    """
    p = Path(filepath)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def current_timestamp(fmt: str = "%Y%m%d%H%M%S") -> str:
    """
    Returns the current timestamp as a string formatted by fmt.

    Args:
        fmt (str): Format string compatible with datetime.strftime.

    Returns:
        str: Formatted current timestamp.
    """
    return datetime.now().strftime(fmt)

def validate_non_empty_string(s: str) -> bool:
    """
    Validates if a string is non-empty and not just whitespace.

    Args:
        s (str): String to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(s and s.strip())
