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
        # A CORREÇÃO ESTÁ AQUI: self.test_dir é agora um objeto Path
        cls.test_dir = Path(tempfile.mkdtemp(prefix="offjournal_test_"))
        # Override the global ENTRIES_DIR to our temp directory
        entry.ENTRIES_DIR = cls.test_dir

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory after all tests are done."""
        shutil.rmtree(cls.test_dir)

    def tearDown(self):
        """Clean up all created files after each test."""
        # Agora self.test_dir é um objeto Path e o .glob() vai funcionar
        for item in self.test_dir.glob('*'):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def test_create_entry_success(self):
        """Test successful creation of a new entry."""
        result = entry.create_entry("Test Title")
        self.assertEqual(result["status"], "success")
        filepath = self.test_dir / result["data"]["filename"]
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
        # Newest first
        self.assertEqual(entries[0]["title"], "Entry Two")

    def test_get_and_update_content(self):
        """Test the cycle of getting, updating, and re-getting content."""
        entry_id = entry.create_entry("Content Test")["data"]["id"]
        
        initial_content = entry.get_entry_content(entry_id)
        self.assertIn("Content Test", initial_content)
        
        new_content = "Updated content here."
        update_result = entry.update_entry_content(entry_id, new_content)
        self.assertEqual(update_result["status"], "success")
        
        final_content = entry.get_entry_content(entry_id)
        self.assertEqual(final_content, new_content)

    def test_delete_entry(self):
        """Test deleting an entry."""
        entry_id = entry.create_entry("To Be Deleted")["data"]["id"]
        self.assertEqual(len(entry.get_entries()), 1)
        
        delete_result = entry.delete_entry(entry_id)
        self.assertEqual(delete_result["status"], "success")
        
        self.assertEqual(len(entry.get_entries()), 0)

if __name__ == "__main__":
    unittest.main()