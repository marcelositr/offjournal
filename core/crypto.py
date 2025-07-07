# core/crypto.py
"""
Encryption module for offjournal.

Provides GPG-based encryption and decryption for journal entries or any file.
Functions return a dictionary indicating the operation's status.

Dependencies:
- gpg (must be installed and in the system's $PATH)
"""

import subprocess
from pathlib import Path

def encrypt_file(filepath: str, recipient: str) -> dict:
    """
    Encrypts a file using GPG for the given recipient.

    Args:
        filepath (str): Path to the file to encrypt.
        recipient (str): GPG key ID or email of the recipient.

    Returns:
        dict: A status dictionary.
    """
    path = Path(filepath)
    if not path.exists():
        return {"status": "error", "message": f"Arquivo não encontrado: {filepath}"}

    encrypted_path = path.with_suffix(path.suffix + ".gpg")

    try:
        result = subprocess.run(
            [
                "gpg", "--yes", "--output", str(encrypted_path),
                "--encrypt", "--recipient", recipient, str(path)
            ],
            capture_output=True,
            text=True,
            check=True  # This will raise CalledProcessError if gpg fails
        )
        return {
            "status": "success",
            "message": f"Arquivo criptografado com sucesso em {encrypted_path.name}",
            "output_path": str(encrypted_path)
        }
    except FileNotFoundError:
        return {"status": "error", "message": "Comando 'gpg' não encontrado. GnuPG está instalado e no seu PATH?"}
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        return {
            "status": "error",

            "message": f"Falha na criptografia: {error_message}"
        }

def decrypt_file(filepath: str) -> dict:
    """
    Decrypts a GPG-encrypted file.

    Args:
        filepath (str): Path to the encrypted .gpg file.

    Returns:
        dict: A status dictionary.
    """
    path = Path(filepath)
    if not path.exists():
        return {"status": "error", "message": f"Arquivo não encontrado: {filepath}"}

    if not filepath.endswith(".gpg"):
        return {"status": "error", "message": "O arquivo especificado não tem a extensão .gpg."}

    # Remove .gpg extension for the output file
    output_path = path.with_suffix("")
    
    try:
        result = subprocess.run(
            [
                "gpg", "--yes", "--output", str(output_path),
                "--decrypt", str(path)
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "success",
            "message": f"Arquivo descriptografado com sucesso em {output_path.name}",
            "output_path": str(output_path)
        }
    except FileNotFoundError:
        return {"status": "error", "message": "Comando 'gpg' não encontrado. GnuPG está instalado e no seu PATH?"}
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        return {
            "status": "error",
            "message": f"Falha na descriptografia: {error_message}"
        }
