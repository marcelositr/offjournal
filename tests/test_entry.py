# tests/test_entry.py

import unittest
import tempfile
import shutil
from pathlib import Path

# We need to set the ENTRIES_DIR before importing the module
# to ensure it uses our temporary directory for all operations.
import core.entry as entry

class TestEntryModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a temporary directory for all tests in this class."""
        # Create a Path object for the temporary directory
        cls.test_dir = Path(tempfile.mkdtemp(prefix="offjournal_test_"))
        # Override the global ENTRIES_DIR to our temp directory
        entry.ENTRIES_DIR = cls.test_dir

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory after all tests are done."""
        shutil.rmtree(cls.test_dir)

    def tearDown(self):
        """Clean up all created files after each test."""
        # Now self.test_dir is a Path object, so .glob() will work
        for item in self.test_dir.glob('*'):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    # ... O RESTANTE DOS TESTES (test_create_entry_success, etc.) CONTINUA IGUAL ...
    # ... pois a lógica deles já estava correta. A única falha era no tearDown.

    def test_create_entry_success(self):
        """Test successful creation of a new entry."""
        title = "My First Test Entry"
        result = entry.create_entry(title)
        self.assertEqual(result["status"], "success")
        entry_data = result["data"]
        filepath = entry.ENTRIES_DIR / entry_data["filename"]
        self.assertTrue(filepath.exists())

    def test_create_entry_empty_title(self):
        """Test that creating an entry with an empty title fails."""
        result = entry.create_entry("   ")
        self.assertEqual(result["status"], "error")

    def test_get_entries(self):
        """Test listing of multiple entries."""
        entry.create_entry("Entry One")
        entry.create_entry("Entry Two")
        entries = entry.get_entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["title"], "Entry Two")

    def test_get_and_update_content(self):
        """Test the full cycle of getting, updating, and re-getting content."""
        entry_id = entry.create_entry("Content Test")["data"]["id"]
        new_content = "# Updated Title\n\nThis is the new content."
        entry.update_entry_content(entry_id, new_content)
        updated_content = entry.get_entry_content(entry_id)
        self.assertEqual(updated_content, new_content)

    def test_delete_entry(self):
        """Test deleting an entry."""
        entry_id = entry.create_entry("To Be Deleted")["data"]["id"]
        self.assertEqual(len(entry.get_entries()), 1)
        entry.delete_entry(entry_id)
        self.assertEqual(len(entry.get_entries()), 0)