# tests/test_media.py

import unittest
import tempfile
import shutil
from pathlib import Path

import core.media as media

class TestMediaModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_base_dir = tempfile.mkdtemp(prefix="offjournal_media_test_")
        media.MEDIA_DIR = Path(cls.test_base_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_base_dir)

    def setUp(self):
        self.entry_id = "20250715120000_test_entry"
        self.source_media_file = media.MEDIA_DIR / "source_image.jpg"
        self.source_media_file.write_text("dummy image content")

    def tearDown(self):
        entry_media_dir = media.MEDIA_DIR / self.entry_id
        if entry_media_dir.exists():
            shutil.rmtree(entry_media_dir)
        if self.source_media_file.exists():
            self.source_media_file.unlink()

    def test_add_list_remove_cycle(self):
        # Add media
        add_result = media.add_media(self.entry_id, str(self.source_media_file))
        self.assertEqual(add_result["status"], "success")

        # List media
        list_result = media.list_media(self.entry_id)
        self.assertEqual(list_result["status"], "success")
        self.assertIn(self.source_media_file.name, list_result["data"])

        # Remove media
        remove_result = media.remove_media(self.entry_id, self.source_media_file.name)
        self.assertEqual(remove_result["status"], "success")

        # Verify it's gone
        final_list = media.list_media(self.entry_id)
        self.assertEqual(len(final_list["data"]), 0)