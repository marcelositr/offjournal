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
        cls.test_dir = tempfile.mkdtemp(prefix="offjournal_test_")
        # Override the global ENTRIES_DIR to our temp directory
        entry.ENTRIES_DIR = Path(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory after all tests are done."""
        shutil.rmtree(cls.test_dir)

    def tearDown(self):
        """Clean up all created files after each test."""
        for item in self.test_dir.glob('*'):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def test_create_entry_success(self):
        """Test successful creation of a new entry."""
        title = "My First Test Entry"
        result = entry.create_entry(title)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        
        entry_data = result["data"]
        self.assertEqual(entry_data["title"], title)
        
        # Verify the file was actually created
        filepath = entry.ENTRIES_DIR / entry_data["filename"]
        self.assertTrue(filepath.exists())
        self.assertIn(f"# {title}", filepath.read_text())

    def test_create_entry_empty_title(self):
        """Test that creating an entry with an empty title fails."""
        result = entry.create_entry("   ") # Title with only spaces
        self.assertEqual(result["status"], "error")
        self.assertIn("título não pode ser vazio", result["message"])

    def test_get_entries(self):
        """Test listing of multiple entries."""
        # Check initial state (should be empty)
        self.assertEqual(entry.get_entries(), [])

        # Create some entries
        entry.create_entry("Entry One")
        entry.create_entry("Entry Two")

        entries = entry.get_entries()
        self.assertEqual(len(entries), 2)
        
        # Entries are sorted newest first, so "Entry Two" should be first
        self.assertEqual(entries[0]["title"], "Entry Two")
        self.assertEqual(entries[1]["title"], "Entry One")

    def test_find_entry_path(self):
        """Test finding an entry's path by its ID."""
        result = entry.create_entry("Find Me")
        entry_id = result["data"]["id"]

        filepath = entry.find_entry_path(entry_id)
        self.assertIsNotNone(filepath)
        self.assertTrue(filepath.exists())

        # Test with a non-existent ID
        self.assertIsNone(entry.find_entry_path("nonexistent123"))

    def test_get_and_update_content(self):
        """Test the full cycle of getting, updating, and re-getting content."""
        create_result = entry.create_entry("Content Test")
        entry_id = create_result["data"]["id"]

        # 1. Get initial content
        initial_content = entry.get_entry_content(entry_id)
        self.assertIn("# Content Test", initial_content)
        self.assertIn("Escreva seus pensamentos aqui...", initial_content)

        # 2. Update the content
        new_content = "# Updated Title\n\nThis is the new content."
        update_result = entry.update_entry_content(entry_id, new_content)
        self.assertEqual(update_result["status"], "success")

        # 3. Get the updated content and verify it
        updated_content = entry.get_entry_content(entry_id)
        self.assertEqual(updated_content, new_content)

    def test_update_non_existent_entry(self):
        """Test updating an entry that does not exist."""
        result = entry.update_entry_content("nonexistent123", "some content")
        self.assertEqual(result["status"], "error")
        self.assertIn("Entry not found", result["message"])

    def test_delete_entry(self):
        """Test deleting an entry."""
        create_result = entry.create_entry("To Be Deleted")
        entry_id = create_result["data"]["id"]

        # Ensure it exists before deleting
        self.assertEqual(len(entry.get_entries()), 1)

        # Delete it
        delete_result = entry.delete_entry(entry_id)
        self.assertEqual(delete_result["status"], "success")

        # Ensure it's gone
        self.assertEqual(len(entry.get_entries()), 0)
        self.assertIsNone(entry.find_entry_path(entry_id))

    def test_delete_non_existent_entry(self):
        """Test deleting an entry that does not exist."""
        result = entry.delete_entry("nonexistent123")
        self.assertEqual(result["status"], "error")
        self.assertIn("Entrada não encontrada", result["message"])

if __name__ == "__main__":
    unittest.main()