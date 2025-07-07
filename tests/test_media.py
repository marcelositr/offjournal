import unittest
import tempfile
import shutil
from pathlib import Path
import core.media as media

class TestMediaModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        media.MEDIA_DIR = Path(self.temp_dir.name) / "media"
        media.MEDIA_DIR.mkdir(parents=True, exist_ok=True)
        self.entry_id = "test_entry"
        self.test_file_path = Path(self.temp_dir.name) / "test_media.txt"
        self.test_file_path.write_text("dummy media content", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_media(self):
        media.add_media(self.entry_id, str(self.test_file_path))
        dest_file = media.MEDIA_DIR / self.entry_id / self.test_file_path.name
        self.assertTrue(dest_file.exists())

    def test_list_media(self):
        media.add_media(self.entry_id, str(self.test_file_path))
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        media.list_media(self.entry_id)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn(self.test_file_path.name, output)

    def test_remove_media(self):
        media.add_media(self.entry_id, str(self.test_file_path))
        media.remove_media(self.entry_id, self.test_file_path.name)
        dest_file = media.MEDIA_DIR / self.entry_id / self.test_file_path.name
        self.assertFalse(dest_file.exists())

if __name__ == "__main__":
    unittest.main()
