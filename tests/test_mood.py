import unittest
import tempfile
from pathlib import Path
import core.mood as mood

class TestMoodModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        mood.ENTRIES_DIR = Path(self.temp_dir.name)

        # Cria duas entradas: uma com palavras positivas e outra negativas
        (mood.ENTRIES_DIR / "20250706120000_positive.md").write_text(
            "I am very happy and excited today!", encoding="utf-8")
        (mood.ENTRIES_DIR / "20250706120001_negative.md").write_text(
            "I feel sad and frustrated.", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_analyze_specific_entry(self):
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output

        mood.analyze_mood("20250706120000_positive")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Positive", output)

    def test_analyze_all_entries(self):
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output

        mood.analyze_mood()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Positive", output)
        self.assertIn("Negative", output)

    def test_entry_not_found(self):
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output

        mood.analyze_mood("nonexistent")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Entry 'nonexistent' not found", output)

if __name__ == "__main__":
    unittest.main()

