# tests/test_planner.py

import unittest
import tempfile
import json
from pathlib import Path

# Override PLANNER_FILE before importing
import core.planner as planner

class TestPlannerModule(unittest.TestCase):
    def setUp(self):
        """Create a temporary file for the planner JSON for each test."""
        # We create a temporary directory to hold our planner file
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        
        # Override the global PLANNER_FILE path
        planner.PLANNER_FILE = self.temp_dir / "planner.json"

    def tearDown(self):
        """Clean up the temporary directory and file."""
        self.temp_dir_obj.cleanup()

    def test_get_events_empty(self):
        """Test getting events when the planner file doesn't exist."""
        events = planner.get_events()
        self.assertEqual(events, [])

    def test_add_event_success(self):
        """Test successfully adding a new event."""
        result = planner.add_event("2025-12-25", "Natal")
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertEqual(result["data"]["title"], "Natal")
        self.assertEqual(result["data"]["id"], 1)

        # Verify it was saved correctly
        events = planner.get_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Natal")

    def test_add_event_invalid_date(self):
        """Test adding an event with an invalid date format."""
        result = planner.add_event("25-12-2025", "Data Inválida")
        self.assertEqual(result["status"], "error")
        self.assertIn("Formato de data inválido", result["message"])

    def test_add_event_empty_title(self):
        """Test adding an event with an empty title."""
        result = planner.add_event("2025-01-01", "  ")
        self.assertEqual(result["status"], "error")
        self.assertIn("título do evento não pode ser vazio", result["message"])

    def test_list_multiple_events(self):
        """Test that get_events returns multiple added events correctly."""
        planner.add_event("2026-01-01", "Ano Novo 2026")
        planner.add_event("2025-10-31", "Halloween")
        
        events = planner.get_events()
        self.assertEqual(len(events), 2)
        
        # The list should be sorted by date
        self.assertEqual(events[0]["title"], "Halloween")
        self.assertEqual(events[1]["title"], "Ano Novo 2026")

    def test_delete_event_success(self):
        """Test successfully deleting an event."""
        add_result = planner.add_event("2025-07-15", "Para Deletar")
        event_id = add_result["data"]["id"]
        
        # Delete it
        delete_result = planner.delete_event(event_id)
        self.assertEqual(delete_result["status"], "success")

        # Verify it's gone
        events = planner.get_events()
        self.assertEqual(len(events), 0)
        
    def test_delete_non_existent_event(self):
        """Test deleting an event ID that does not exist."""
        planner.add_event("2025-01-01", "Evento Existente")
        result = planner.delete_event(999) # Non-existent ID
        self.assertEqual(result["status"], "error")
        self.assertIn("não encontrado", result["message"])

    def test_update_event_success(self):
        """Test successfully updating an event's title and date."""
        add_result = planner.add_event("2025-01-01", "Título Antigo")
        event_id = add_result["data"]["id"]

        # Update title
        update_title_result = planner.update_event(event_id, title="Título Novo")
        self.assertEqual(update_title_result["status"], "success")
        
        # Update date
        update_date_result = planner.update_event(event_id, date_str="2026-02-02")
        self.assertEqual(update_date_result["status"], "success")

        # Verify changes
        events = planner.get_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Título Novo")
        self.assertEqual(events[0]["date"], "2026-02-02")

    def test_update_non_existent_event(self):
        """Test updating an event that does not exist."""
        result = planner.update_event(999, title="Novo Título")
        self.assertEqual(result["status"], "error")
        self.assertIn("não encontrado", result["message"])
        
if __name__ == "__main__":
    unittest.main()