# tests/test_utils.py

import unittest
import tempfile
from pathlib import Path
import core.utils as utils

class TestUtilsModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)

    def tearDown(self):
        self.temp_dir_obj.cleanup()

    def test_ensure_dir_creates_directory(self):
        """Test that ensure_dir creates a non-existent directory."""
        new_dir_path = self.temp_dir / "new_dir"
        self.assertFalse(new_dir_path.exists())
        
        utils.ensure_dir(str(new_dir_path))
        
        self.assertTrue(new_dir_path.exists())
        self.assertTrue(new_dir_path.is_dir())

    def test_ensure_dir_does_not_fail_on_existing(self):
        """Test that ensure_dir does not raise an error if the directory already exists."""
        # It's already created by setUp
        try:
            utils.ensure_dir(str(self.temp_dir))
        except Exception as e:
            self.fail(f"ensure_dir() raised an unexpected exception on an existing directory: {e}")

    def test_read_and_write_file(self):
        """Test the cycle of writing to and reading from a file."""
        test_file = self.temp_dir / "testfile.txt"
        content = "Hello, off.journal!\nThis is a test."
        
        utils.write_file(str(test_file), content)
        
        read_content = utils.read_file(str(test_file))
        self.assertEqual(content, read_content)

    def test_read_file_not_found(self):
        """Test that read_file raises FileNotFoundError for a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            utils.read_file(str(self.temp_dir / "nonexistent_file.txt"))

    def test_get_current_timestamp_format(self):
        """Test the format of the generated timestamp."""
        # Test default format
        ts_default = utils.get_current_timestamp()
        self.assertRegex(ts_default, r"\d{14}") # e.g., 20250715103000

        # Test custom format
        ts_custom = utils.get_current_timestamp(fmt="%Y-%m-%d")
        self.assertRegex(ts_custom, r"\d{4}-\d{2}-\d{2}") # e.g., 2025-07-15

    def test_validate_non_empty_string(self):
        """Test the string validation utility."""
        self.assertTrue(utils.validate_non_empty_string("valid"))
        self.assertTrue(utils.validate_non_empty_string("  valid  "))
        self.assertFalse(utils.validate_non_empty_string(""))
        self.assertFalse(utils.validate_non_empty_string("   "))
        self.assertFalse(utils.validate_non_empty_string(None))

if __name__ == "__main__":
    unittest.main()
