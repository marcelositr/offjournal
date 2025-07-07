# tests/test_crypto.py

import unittest
import tempfile
import shutil
from pathlib import Path
import core.crypto as crypto

# Helper para verificar se o comando gpg está disponível no sistema
def is_gpg_available():
    return shutil.which("gpg") is not None

class TestCryptoModule(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test.txt"
        self.test_file.write_text("This is a crypto test file.")
        self.recipient = "test@example.com" # Destinatário de teste

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_encrypt_file_not_exist(self):
        """Test that encrypting a non-existent file returns an error status."""
        # CORREÇÃO: Verificamos o dicionário de retorno, não os logs.
        result = crypto.encrypt_file("nonexistent_file.txt", self.recipient)
        self.assertEqual(result["status"], "error")
        self.assertIn("Arquivo não encontrado", result["message"])

    @unittest.skipUnless(is_gpg_available(), "GnuPG (gpg) não encontrado no PATH, pulando teste.")
    def test_encrypt_with_invalid_recipient(self):
        """Test encryption with a non-existent recipient key."""
        # Este teste é útil para verificar se os erros do GPG são capturados.
        invalid_recipient = "nobody@invalid-domain-that-does-not-exist-123.com"
        result = crypto.encrypt_file(str(self.test_file), invalid_recipient)
        self.assertEqual(result["status"], "error")
        # O GPG geralmente retorna "No public key" ou similar nesta situação.
        self.assertIn("public key", result["message"].lower())
    
    # CORREÇÃO: Marcamos este teste para ser pulado por padrão.
    # Ele requer uma configuração manual de chaves GPG no ambiente de execução,
    # o que não é prático para um CI simples.
    @unittest.skip("Pulando teste de ciclo GPG, requer configuração manual de chaves.")
    def test_encrypt_decrypt_cycle(self):
        """
        Testa o ciclo completo de criptografia e descriptografia.
        Pode ser executado localmente se você tiver uma chave para o destinatário.
        """
        encrypt_result = crypto.encrypt_file(str(self.test_file), self.recipient)
        self.assertEqual(encrypt_result["status"], "success", f"Falha na criptografia: {encrypt_result.get('message')}")
        
        encrypted_file_path = Path(encrypt_result["output_path"])
        self.assertTrue(encrypted_file_path.exists())

        self.test_file.unlink() # Remove o original para garantir que a descriptografia funcione

        decrypt_result = crypto.decrypt_file(str(encrypted_file_path))
        self.assertEqual(decrypt_result["status"], "success", f"Falha na descriptografia: {decrypt_result.get('message')}")
        
        decrypted_file_path = Path(decrypt_result["output_path"])
        self.assertTrue(decrypted_file_path.exists())
        self.assertEqual(decrypted_file_path.read_text(), "This is a crypto test file.")

if __name__ == "__main__":
    unittest.main()