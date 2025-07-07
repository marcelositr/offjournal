# tests/test_mood.py

import unittest
import tempfile
import shutil
from pathlib import Path

# Override ENTRIES_DIR before importing the module
import core.mood as mood

class TestMoodModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary directory for all mood analysis tests."""
        cls.test_dir = tempfile.mkdtemp(prefix="offjournal_mood_test_")
        # Override the global ENTRIES_DIR to our temp directory
        mood.ENTRIES_DIR = Path(cls.test_dir)

        # Create a positive and a negative entry for testing
        cls.positive_id = "20250715100000"
        (mood.ENTRIES_DIR / f"{cls.positive_id}_positive_day.md").write_text(
            "# Dia Incrível\n\nEstou muito feliz e animado hoje! Que dia fantástico.", 
            encoding="utf-8"
        )

        cls.negative_id = "20250715100100"
        (mood.ENTRIES_DIR / f"{cls.negative_id}_negative_day.md").write_text(
            "# Dia Ruim\n\nMe sinto triste e frustrado. Foi um dia péssimo.",
            encoding="utf-8"
        )
        
        cls.neutral_id = "20250715100200"
        (mood.ENTRIES_DIR / f"{cls.neutral_id}_neutral_day.md").write_text(
            "# Apenas um Dia\n\nO dia foi normal, sem grandes eventos.",
            encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory after all tests."""
        shutil.rmtree(cls.test_dir)

    def test_analyze_positive_entry(self):
        """Test mood analysis on a predominantly positive entry."""
        result = mood.analyze_entry_mood(self.positive_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["mood"], "Positivo")
        self.assertGreater(result["positive_score"], result["negative_score"])

    def test_analyze_negative_entry(self):
        """Test mood analysis on a predominantly negative entry."""
        result = mood.analyze_entry_mood(self.negative_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["mood"], "Negativo")
        self.assertGreater(result["negative_score"], result["positive_score"])

    def test_analyze_neutral_entry(self):
        """Test mood analysis on a neutral entry with no keywords."""
        result = mood.analyze_entry_mood(self.neutral_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["mood"], "Neutro")
        self.assertEqual(result["positive_score"], 0)
        self.assertEqual(result["negative_score"], 0)

    def test_analyze_non_existent_entry(self):
        """Test analyzing an entry that does not exist."""
        result = mood.analyze_entry_mood("nonexistent123")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("não encontrada", result["message"])

if __name__ == "__main__":
    unittest.main()