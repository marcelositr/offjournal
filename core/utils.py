# core/utils.py
"""
Utility functions for offjournal.
Provides generic helper functions to support other modules.
"""
from pathlib import Path
from datetime import datetime

def ensure_dir(path: str) -> None:
    """Ensures a directory exists, creating it if necessary."""
    Path(path).mkdir(parents=True, exist_ok=True)

def read_file(filepath: str) -> str:
    """Reads the content of a text file."""
    return Path(filepath).read_text(encoding="utf-8")

def write_file(filepath: str, content: str) -> None:
    """Writes content to a text file, overwriting if it exists."""
    Path(filepath).write_text(content, encoding="utf-8")

def get_current_timestamp(fmt: str = "%Y%m%d%H%M%S") -> str: # <--- NOME CORRIGIDO AQUI
    """Returns the current timestamp as a formatted string."""
    return datetime.now().strftime(fmt)

def validate_non_empty_string(s: str) -> bool:
    """Validates if a string is non-empty and not just whitespace."""
    return bool(s and s.strip())