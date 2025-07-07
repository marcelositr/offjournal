# core/export.py
"""
Export module for offjournal.

Provides functionality to export journal entries to various formats:
TXT, Markdown (MD), and JSON.
Functions return a dictionary indicating the operation's status.
"""

import json
from pathlib import Path

def _copy_text(input_file: str, output_file: str) -> dict:
    """
    Helper function to copy text from one file to another.
    Returns a status dictionary.
    """
    input_path = Path(input_file)
    if not input_path.exists():
        return {"status": "error", "message": f"Arquivo de entrada não encontrado: {input_file}"}

    try:
        with open(input_path, "r", encoding="utf-8") as src, \
             open(output_file, "w", encoding="utf-8") as dst:
            dst.write(src.read())
        return {"status": "success", "message": f"Exportado com sucesso para: {output_file}"}
    except IOError as e:
        return {"status": "error", "message": f"Erro de E/S ao exportar: {e}"}

def export_to_txt(input_file: str, output_file: str) -> dict:
    """
    Exports content to a .txt file.

    Args:
        input_file (str): Path to the source entry file.
        output_file (str): Destination file path.

    Returns:
        dict: A status dictionary.
    """
    return _copy_text(input_file, output_file)

def export_to_md(input_file: str, output_file: str) -> dict:
    """
    Exports content to a .md (Markdown) file.

    Args:
        input_file (str): Path to the source entry file.
        output_file (str): Destination file path.

    Returns:
        dict: A status dictionary.
    """
    return _copy_text(input_file, output_file)

def export_to_json(input_file: str, output_file: str) -> dict:
    """
    Exports content to a .json file. The input file is wrapped as a JSON object.

    Args:
        input_file (str): Path to the source entry file.
        output_file (str): Destination file path.

    Returns:
        dict: A status dictionary.
    """
    input_path = Path(input_file)
    if not input_path.exists():
        return {"status": "error", "message": f"Arquivo de entrada não encontrado: {input_file}"}

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        data = {
            "source_filename": input_path.name,
            "export_format": "json",
            "content": content
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {"status": "success", "message": f"Exportado para JSON com sucesso: {output_file}"}
    except IOError as e:
        return {"status": "error", "message": f"Erro de E/S ao exportar para JSON: {e}"}
    except TypeError as e:
        return {"status": "error", "message": f"Erro ao serializar para JSON: {e}"}
