# core/mood.py
"""
Mood analysis module for offjournal.

Provides a simple sentiment analysis of journal entries based on keyword matching.
"""

from pathlib import Path

# This should point to the same directory as in core/entry.py
ENTRIES_DIR = Path.home() / ".offjournal" / "entries"

# Simple word lists for positive and negative sentiment
# (in Portuguese, to match potential user input)
POSITIVE_WORDS = {"feliz", "alegre", "amor", "animado", "ótimo", "bom", "incrível", "fantástico", "sucesso", "grato", "orgulhoso"}
NEGATIVE_WORDS = {"triste", "raiva", "chateado", "ruim", "péssimo", "ódio", "deprimido", "terrível", "frustrado", "medo", "ansioso"}

def _find_entry_path(entry_id: str) -> Path | None:
    """Helper to find an entry path by its ID. Avoids code duplication."""
    if not entry_id or not entry_id.strip():
        return None
    matches = list(ENTRIES_DIR.glob(f"{entry_id}*.md"))
    return matches[0] if matches else None

def analyze_entry_mood(entry_id: str) -> dict:
    """
    Analyzes the mood of a specific journal entry.

    Args:
        entry_id (str): The ID (timestamp prefix) of the entry to analyze.

    Returns:
        A dictionary with the mood analysis results or an error.
        Example: {"status": "success", "mood": "Positive", "positive": 5, "negative": 1}
    """
    filepath = _find_entry_path(entry_id)
    if not filepath:
        return {"status": "error", "message": f"Entrada '{entry_id}' não encontrada."}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # Normalize text to lowercase for case-insensitive matching
            text = f.read().lower()

        positive_count = sum(word in text for word in POSITIVE_WORDS)
        negative_count = sum(word in text for word in NEGATIVE_WORDS)

        mood = "Neutro"
        if positive_count > negative_count:
            mood = "Positivo"
        elif negative_count > positive_count:
            mood = "Negativo"

        return {
            "status": "success",
            "entry_id": entry_id,
            "filename": filepath.name,
            "mood": mood,
            "positive_score": positive_count,
            "negative_score": negative_count
        }
    except IOError as e:
        return {"status": "error", "message": f"Não foi possível ler o arquivo da entrada: {e}"}

# Note: The function to analyze *all* entries can be built on top of this one
# by the calling interface (e.g., iterating through all entry IDs and calling this).
# This keeps the core module focused on single-entry operations.
