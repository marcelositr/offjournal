import unittest
import tempfile
from pathlib import Path
import core.export as export

class TestExportModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_file = Path(self.temp_dir.name) / "entry.md"
        self.input_file.write_text("Test content", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_export_to_txt(self):
        output_file = Path(self.temp_dir.name) / "output.txt"
        export.export_to_txt(str(self.input_file), str(output_file))
        self.assertTrue(output_file.exists())
        self.assertEqual(output_file.read_text(encoding="utf-8"), "Test content")

    def test_export_to_md(self):
        output_file = Path(self.temp_dir.name) / "output.md"
        export.export_to_md(str(self.input_file), str(output_file))
        self.assertTrue(output_file.exists())
        self.assertEqual(output_file.read_text(encoding="utf-8"), "Test content")

    def test_export_to_json(self):
        output_file = Path(self.temp_dir.name) / "output.json"
        export.export_to_json(str(self.input_file), str(output_file))
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding="utf-8")
        self.assertIn("Test content", content)

if __name__ == "__main__":
    unittest.main()
