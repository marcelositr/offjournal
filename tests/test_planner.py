import unittest
import tempfile
import shutil
import json
from pathlib import Path
import core.planner as planner

class TestPlannerModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.planner_file = Path(self.temp_dir.name) / "planner.json"
        planner.PLANNER_FILE = self.planner_file

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_event(self):
        planner.add_event("2025-07-10", "Test Event")
        events = planner._load_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Test Event")

        # Capturar saída de list_events
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        planner.list_events()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Test Event", output)

    def test_edit_event(self):
        planner.add_event("2025-07-10", "Old Title")
        events = planner._load_events()
        event_id = events[0]["id"]
        planner.edit_event(event_id, title="New Title")

        events = planner._load_events()
        self.assertEqual(events[0]["title"], "New Title")

    def test_remove_event(self):
        planner.add_event("2025-07-10", "To be removed")
        events = planner._load_events()
        event_id = events[0]["id"]
        planner.remove_event(event_id)
        events = planner._load_events()
        self.assertEqual(len(events), 0)

if __name__ == "__main__":
    unittest.main()
