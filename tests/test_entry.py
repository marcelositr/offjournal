# tests/test_entry.py

import unittest
import tempfile
import shutil
import os
from pathlib import Path
import core.entry as entry

class TestEntryModule(unittest.TestCase):

    def setUp(self):
        # Cria diretório temporário e muda o ENTRIES_DIR para lá
        self.test_dir = tempfile.mkdtemp()
        entry.ENTRIES_DIR = Path(self.test_dir)

    def tearDown(self):
        # Remove diretório temporário após testes
        shutil.rmtree(self.test_dir)

    def test_create_entry(self):
        title = "Test Entry"
        entry.create_entry(title)
        files = list(entry.ENTRIES_DIR.glob("*.md"))
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].name.endswith("_Test_Entry.md"))

    def test_list_entries(self):
        # Criar algumas entradas pra testar listagem
        titles = ["Entry One", "Entry Two"]
        for t in titles:
            entry.create_entry(t)

        # Capturar output de list_entries
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        entry.list_entries()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Entry_One.md", output)
        self.assertIn("Entry_Two.md", output)

    def test_edit_entry_not_found(self):
        # Testar editar entrada inexistente
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        entry.edit_entry("99999999999999")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Entry not found", output)

if __name__ == "__main__":
    unittest.main()
