# core/entry.py
"""
Entry management module for offjournal.

Provides functionality to create, edit, list, and manage journal entries.
All functions are designed to return structured data (lists or dicts)
to be used by any frontend (CLI, GUI, etc.).
"""
import os
from datetime import datetime
from pathlib import Path

# Base directory for all journal entries
ENTRIES_DIR = Path.home() / ".offjournal" / "entries"
ENTRIES_DIR.mkdir(parents=True, exist_ok=True)


def _parse_filename(path: Path) -> dict:
    """
    Extracts structured data (id, title) from a filename.
    Example: "20250715100000_My_First_Entry.md" ->
             {"id": "20250715100000", "title": "My First Entry"}
    """
    parts = path.stem.split('_', 1)
    return {
        "id": parts[0],
        "title": parts[1].replace('_', ' ') if len(parts) > 1 else "Sem Título",
        "filename": path.name
    }

def get_entries() -> list[dict]:
    """
    Returns a list of all journal entries, with newest first.
    Each entry is a dictionary containing its id, title, and filename.
    """
    try:
        files = sorted(ENTRIES_DIR.glob("*.md"), reverse=True)
        return [_parse_filename(f) for f in files]
    except OSError:
        return []

def find_entry_path(entry_id: str) -> Path | None:
    """
    Finds the full path of an entry by its ID prefix.
    Returns the Path object or None if not found.
    """
    if not entry_id or not entry_id.strip():
        return None
    
    # Use glob to find any file starting with the ID
    matches = list(ENTRIES_DIR.glob(f"{entry_id}*.md"))
    return matches[0] if matches else None

def get_entry_content(entry_id: str) -> str | None:
    """
    Returns the raw string content of a specific journal entry.
    Returns None if the entry is not found.
    """
    filepath = find_entry_path(entry_id)
    if not filepath:
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except IOError:
        return None

def update_entry_content(entry_id: str, new_content: str) -> dict:
    """
    Updates the content of an existing journal entry.
    Returns a dictionary with the status of the operation.
    """
    filepath = find_entry_path(entry_id)
    if not filepath:
        return {"status": "error", "message": "Entry not found."}

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return {"status": "success", "message": "Entrada salva com sucesso."}
    except IOError as e:
        return {"status": "error", "message": f"Falha ao escrever no arquivo: {e}"}

def create_entry(title: str) -> dict:
    """
    Creates a new journal entry and returns its data.
    Returns a dictionary with status and entry data or an error message.
    """
    if not title or not title.strip():
        return {"status": "error", "message": "O título não pode ser vazio."}

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_title = "_".join(title.strip().split())
    filename = f"{timestamp}_{safe_title}.md"
    filepath = ENTRIES_DIR / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title.strip()}\n\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Escreva seus pensamentos aqui...\n")
        
        return {
            "status": "success",
            "data": _parse_filename(filepath)
        }
    except IOError as e:
        return {"status": "error", "message": f"Falha ao criar a entrada: {e}"}

def delete_entry(entry_id: str) -> dict:
    """
    Deletes a journal entry by its ID.
    Returns a dictionary with the status of the operation.
    """
    filepath = find_entry_path(entry_id)
    if not filepath:
        return {"status": "error", "message": "Entrada não encontrada."}
    
    try:
        filepath.unlink()
        return {"status": "success", "message": "Entrada excluída com sucesso."}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao excluir a entrada: {e}"}
