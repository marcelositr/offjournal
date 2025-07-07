# core/media.py
"""
Media management module for offjournal.

Handles adding, listing, and removing media attachments linked to journal entries.
All functions return structured data.
"""

import shutil
from pathlib import Path

# Base directory for all media attachments, organized by entry ID
MEDIA_DIR = Path.home() / ".offjournal" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

def add_media(entry_id: str, media_path_str: str) -> dict:
    """
    Adds a media file as an attachment to a journal entry.

    Args:
        entry_id (str): Identifier of the journal entry.
        media_path_str (str): Path to the media file to attach.

    Returns:
        dict: A status dictionary.
    """
    media_file = Path(media_path_str)
    if not media_file.exists():
        return {"status": "error", "message": f"Arquivo de mídia não existe: {media_path_str}"}

    if not entry_id:
        return {"status": "error", "message": "ID da entrada não pode ser vazio."}

    try:
        dest_dir = MEDIA_DIR / entry_id
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / media_file.name
        if dest_file.exists():
            return {"status": "error", "message": f"Arquivo de mídia '{media_file.name}' já existe para esta entrada."}

        shutil.copy2(media_file, dest_file)
        return {"status": "success", "message": f"Mídia '{media_file.name}' adicionada à entrada '{entry_id}'."}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao adicionar mídia: {e}"}

def list_media(entry_id: str) -> dict:
    """
    Lists all media attachments for a journal entry.

    Args:
        entry_id (str): Identifier of the journal entry.

    Returns:
        dict: A status dictionary containing a list of filenames on success.
    """
    if not entry_id:
        return {"status": "error", "message": "ID da entrada não pode ser vazio."}

    media_folder = MEDIA_DIR / entry_id
    if not media_folder.is_dir():
        # It's not an error if a folder doesn't exist, just means no media
        return {"status": "success", "data": []}

    try:
        files = [f.name for f in media_folder.iterdir() if f.is_file()]
        return {"status": "success", "data": sorted(files)}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao listar mídias: {e}"}

def remove_media(entry_id: str, media_filename: str) -> dict:
    """
    Removes a specific media attachment from a journal entry.

    Args:
        entry_id (str): Identifier of the journal entry.
        media_filename (str): Name of the media file to remove.

    Returns:
        dict: A status dictionary.
    """
    if not entry_id or not media_filename:
        return {"status": "error", "message": "ID da entrada e nome da mídia não podem ser vazios."}

    media_file = MEDIA_DIR / entry_id / media_filename
    if not media_file.exists():
        return {"status": "error", "message": f"Arquivo de mídia '{media_filename}' não encontrado para a entrada '{entry_id}'."}

    try:
        media_file.unlink()
        return {"status": "success", "message": f"Mídia '{media_filename}' removida com sucesso."}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao remover mídia: {e}"}
