# core/planner.py
"""
Planner module for offjournal.

Manages an offline agenda with events stored in a JSON file.
All functions return structured data for consumption by any UI.
"""

import json
from pathlib import Path
from datetime import datetime

# Path to the planner data file
PLANNER_FILE = Path.home() / ".offjournal" / "planner.json"

def _load_events() -> list[dict]:
    """
    Loads events from the JSON file.
    Returns an empty list if the file doesn't exist or is invalid.
    """
    if not PLANNER_FILE.exists():
        return []
    try:
        with open(PLANNER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # In case of corruption or read error, treat as empty
        return []

def _save_events(events: list[dict]) -> bool:
    """
    Saves the list of events to the JSON file.
    Returns True on success, False on failure.
    """
    try:
        PLANNER_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PLANNER_FILE, "w", encoding="utf-8") as f:
            # Sort by date before saving for consistency
            sorted_events = sorted(events, key=lambda x: (x.get('date', ''), x.get('id', 0)))
            json.dump(sorted_events, f, indent=2)
        return True
    except IOError:
        return False

def get_events() -> list[dict]:
    """
    Returns all planner events, sorted by date.
    The list is returned directly as it's already structured data.
    """
    return _load_events()

def add_event(date_str: str, title: str) -> dict:
    """
    Adds a new event to the planner.
    Returns a dictionary with status and the newly created event data.
    """
    try:
        # Validate date format
        datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return {"status": "error", "message": "Formato de data inválido. Use AAAA-MM-DD."}
    
    if not title or not title.strip():
        return {"status": "error", "message": "O título do evento não pode ser vazio."}

    events = _load_events()
    new_id = max([ev.get("id", 0) for ev in events], default=0) + 1
    new_event = {"id": new_id, "date": date_str, "title": title.strip()}
    events.append(new_event)
    
    if _save_events(events):
        return {"status": "success", "data": new_event}
    else:
        return {"status": "error", "message": "Falha ao salvar o arquivo do planejador."}

def update_event(event_id: int, date_str: str | None = None, title: str | None = None) -> dict:
    """
    Updates an existing event's date and/or title.
    Returns a status dictionary.
    """
    if not isinstance(event_id, int):
        return {"status": "error", "message": "ID do evento inválido."}

    events = _load_events()
    event_found = False
    for ev in events:
        if ev.get("id") == event_id:
            event_found = True
            if date_str:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    ev["date"] = date_str
                except (ValueError, TypeError):
                    return {"status": "error", "message": "Formato de data inválido. Use AAAA-MM-DD."}
            if title:
                if not title.strip():
                    return {"status": "error", "message": "O título não pode ser vazio."}
                ev["title"] = title.strip()
            break
    
    if not event_found:
        return {"status": "error", "message": f"Evento com ID {event_id} não encontrado."}
    
    if _save_events(events):
        return {"status": "success", "message": f"Evento {event_id} atualizado com sucesso."}
    else:
        return {"status": "error", "message": "Falha ao salvar o arquivo do planejador."}

def delete_event(event_id: int) -> dict:
    """
    Deletes an event from the planner by its ID.
    Returns a status dictionary.
    """
    if not isinstance(event_id, int):
        return {"status": "error", "message": "ID do evento inválido."}

    events = _load_events()
    initial_count = len(events)
    filtered_events = [ev for ev in events if ev.get("id") != event_id]
    
    if len(filtered_events) == initial_count:
        return {"status": "error", "message": f"Evento com ID {event_id} não encontrado."}

    if _save_events(filtered_events):
        return {"status": "success", "message": f"Evento {event_id} removido com sucesso."}
    else:
        return {"status": "error", "message": "Falha ao salvar o arquivo do planejador."}
