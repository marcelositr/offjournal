import unittest
import tempfile
import os
import subprocess
from pathlib import Path
import core.crypto as crypto

class TestCryptoModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test.txt"
        self.test_file.write_text("This is a test file.", encoding="utf-8")
        self.recipient = "test@example.com"  # Troca pelo seu ID de chave GPG real se for testar com chaves reais

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_encrypt_file_not_exist(self):
        # Tenta encriptar arquivo inexistente, espera print de erro
        with self.assertLogs(level='INFO') as log:
            crypto.encrypt_file("nonexistent.file", self.recipient)

    def test_encrypt_decrypt_cycle(self):
        # Esse teste depende de ter chave GPG configurada no sistema
        encrypted_file = self.test_file.with_suffix(".txt.gpg")
        crypto.encrypt_file(str(self.test_file), self.recipient)
        self.assertTrue(encrypted_file.exists())

        # Agora decriptar
        crypto.decrypt_file(str(encrypted_file))
        decrypted_file = self.test_file
        self.assertTrue(decrypted_file.exists())

if __name__ == "__main__":
    unittest.main()
