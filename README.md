# off.journal

**`off.journal`** é um diário e planejador 100% offline, projetado para ser seu companheiro digital privado e seguro. Ele é construído com uma filosofia modular, oferecendo tanto uma interface de linha de comando (CLI) para os amantes do terminal, quanto uma interface gráfica (GUI) moderna e intuitiva para uma experiência mais visual.

![Placeholder para um screenshot da GUI do off.journal]
*(Em breve, um screenshot da interface gráfica)*

---

## ✨ Funcionalidades Principais

-   **Interface Dupla**: Use o `off.journal` da maneira que preferir.
    -   **CLI (Command-Line Interface)**: Rápida, eficiente e totalmente controlável pelo teclado.
    -   **GUI (Graphical User Interface)**: Amigável, visual e fácil de usar, construída com tecnologias web leves (HTML, CSS, JS) e WebKitGTK.
-   **Diário Pessoal**: Crie, leia, edite e apague entradas de diário. As entradas são salvas em formato Markdown, permitindo formatação rica e simples.
-   **Planejador de Eventos**: Gerencie seus compromissos, tarefas e datas importantes de forma simples e direta.
-   **Foco na Privacidade**: Todos os seus dados são salvos localmente, em seu próprio computador. Nada é enviado para a nuvem.
-   **Extensível**: A arquitetura modular permite que novas funcionalidades, como criptografia, exportação e análise de humor, sejam facilmente adicionadas.

---

## 🚀 Como Começar

### 1. Pré-requisitos

-   Python 3.8 ou superior.
-   `git` para clonar o repositório (opcional).

### 2. Instalação

Primeiro, clone ou baixe este repositório para a sua máquina:

```bash
git clone https://github.com/seu-usuario/offjournal.git
cd offjournal
```

O projeto não requer bibliotecas Python externas via `pip` para seu funcionamento básico.

### 3. Usando a Interface Gráfica (GUI)

A GUI é a forma mais recomendada para a maioria dos usuários.

**a) Instale as dependências da GUI:**

A interface gráfica depende de bibliotecas do sistema que devem ser instaladas com o gerenciador de pacotes da sua distribuição Linux:

-   **Para Debian, Ubuntu e derivados:**
    ```bash
    sudo apt update
    sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
    ```

-   **Para Arch Linux e derivados:**
    ```bash
    sudo pacman -Syu python-gobject webkit2gtk
    ```

-   **Para Fedora, CentOS, RHEL:**
    ```bash
    sudo dnf install python3-gobject webkit2gtk4.0
    ```

**b) Execute a aplicação:**

Com as dependências instaladas, inicie a GUI com um único comando:

```bash
python3 main.py gui
```

### 4. Usando a Linha de Comando (CLI)

Para acesso rápido e scripting, a CLI é a ferramenta perfeita.

**Comandos do Diário:**

```bash
# Listar todas as entradas, da mais nova para a mais antiga
python3 main.py listar

# Criar uma nova entrada com o título "Minha Viagem"
python3 main.py nova "Minha Viagem"

# Ler o conteúdo de uma entrada (use o ID da lista)
python3 main.py ler 20250715103000

# Apagar uma entrada (ação irreversível!)
python3 main.py apagar 20250715103000
```

**Comandos do Planejador:**

```bash
# Listar todos os eventos, ordenados por data
python3 main.py planner listar

# Adicionar um novo evento
python3 main.py planner add 2025-12-25 "Ceia de Natal em família"

# Remover um evento pelo seu ID numérico
python3 main.py planner del 1
```

---

## 📁 Onde Meus Dados Ficam?

Sua privacidade é a prioridade. Todos os dados são armazenados de forma transparente no seu diretório `home`, dentro de uma pasta oculta chamada `.offjournal`:

-   **Entradas do Diário**: `~/.offjournal/entries/`
    -   Cada entrada é um arquivo `.md` separado.
-   **Dados do Planejador**: `~/.offjournal/planner.json`
    -   Um único arquivo JSON com todos os seus eventos.
-   **Mídia (Anexos)**: `~/.offjournal/media/`
    -   Os anexos são organizados em subpastas com o ID da entrada correspondente.

---

## 🛠️ Para Desenvolvedores

### Arquitetura do Projeto

O `off.journal` é dividido em duas camadas principais:

1.  **`core/`**: O coração do projeto. É uma biblioteca de lógica pura, sem interface. Todas as funções aqui retornam dados estruturados (dicionários, listas) e não interagem diretamente com o usuário (sem `print()` ou `input()`).
2.  **Interfaces (`main.py` e `offjournal_gui/`)**: São os "clientes" do `core`. Elas chamam as funções do `core`, recebem os dados e os apresentam ao usuário, seja no terminal ou em uma janela gráfica.

Essa separação torna o projeto fácil de testar, manter e estender.

### Executando os Testes

Para garantir a integridade do código, execute a suíte de testes:

```bash
python3 -m unittest discover tests
```

---

## 📄 Licença

Este projeto é licenciado sob a **Licença Pública Geral GNU v3.0 (GPLv3)**. Consulte o arquivo `LICENSE` para mais detalhes.

--- END OF FILE: offjournal/README.md ---

--- START OF FILE: offjournal/main.py ---
# main.py
"""
Main command-line interface (CLI) for offjournal.

This script parses command-line arguments and calls the appropriate
functions from the 'core' package. It also serves as the launcher
for the GUI application.
"""
import argparse
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path to allow importing 'core'
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from core import entry, planner, mood, crypto, export, media

def main_cli():
    """Parses arguments and dispatches to the correct handler."""
    parser = argparse.ArgumentParser(
        prog="offjournal",
        description="off.journal - Seu diário e planejador offline no terminal.",
        epilog="Use 'offjournal <comando> --help' para mais informações sobre um comando específico."
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis", required=True)

    # --- GUI Command ---
    subparsers.add_parser("gui", help="Abrir a interface gráfica do off.journal")

    # --- Entry Commands ---
    parser_new = subparsers.add_parser("nova", help="Criar uma nova entrada no diário")
    parser_new.add_argument("titulo", help="Título da entrada")

    parser_read = subparsers.add_parser("ler", help="Ler o conteúdo de uma entrada")
    parser_read.add_argument("id", help="ID (prefixo do timestamp) da entrada a ser lida")

    subparsers.add_parser("listar", help="Listar todas as entradas do diário")

    parser_delete = subparsers.add_parser("apagar", help="Apagar uma entrada do diário")
    parser_delete.add_argument("id", help="ID da entrada a ser apagada")

    # --- Planner Commands ---
    parser_planner = subparsers.add_parser("planner", help="Acessar o planejador")
    planner_sub = parser_planner.add_subparsers(dest="planner_command", required=True, help="Ações do planejador")
    
    planner_sub.add_parser("listar", help="Listar todos os eventos")
    
    p_add = planner_sub.add_parser("add", help="Adicionar novo evento")
    p_add.add_argument("data", help="Data do evento no formato AAAA-MM-DD")
    p_add.add_argument("titulo", help="Título do evento")
    
    p_del = planner_sub.add_parser("del", help="Remover um evento")
    p_del.add_argument("id", type=int, help="ID numérico do evento a ser removido")

    args = parser.parse_args()

    # --- Command Dispatcher ---
    if args.command == "gui":
        run_gui_app()
    elif args.command == "nova":
        handle_cli_response(entry.create_entry(args.titulo))
    elif args.command == "ler":
        content = entry.get_entry_content(args.id)
        if content is not None:
            print(content)
        else:
            print(f"Erro: Entrada com ID '{args.id}' não encontrada.")
    elif args.command == "listar":
        entries = entry.get_entries()
        if not entries:
            print("Nenhuma entrada no diário encontrada.")
            return
        print("--- Entradas do Diário ---")
        for e in entries:
            print(f"  ID: {e['id']} | Título: {e['title']}")
    elif args.command == "apagar":
        handle_cli_response(entry.delete_entry(args.id))
    elif args.command == "planner":
        handle_planner_command(args)

def handle_planner_command(args):
    """Handles sub-commands for the 'planner' command."""
    if args.planner_command == "listar":
        events = planner.get_events()
        if not events:
            print("Nenhum evento no planejador.")
            return
        print("--- Eventos do Planejador ---")
        for ev in events:
            print(f"  ID: {ev['id']:<3} | Data: {ev['date']} | Título: {ev['title']}")
    elif args.planner_command == "add":
        handle_cli_response(planner.add_event(args.data, args.titulo))
    elif args.planner_command == "del":
        handle_cli_response(planner.delete_event(args.id))

def handle_cli_response(response: dict):
    """Prints a formatted message to the CLI based on a status dictionary."""
    if not isinstance(response, dict):
        print("Erro: Resposta inesperada do módulo core.")
        return

    status = response.get("status")
    message = response.get("message", "Nenhuma mensagem de status recebida.")
    
    if status == "success":
        print(f"Sucesso: {message}")
    elif status == "error":
        print(f"Erro: {message}", file=sys.stderr)
    else:
        if response.get('data'):
             print(f"Operação concluída. Dados: {response['data']}")
        else:
             print(message)

def run_gui_app():
    """Finds and launches the GUI application in a separate process."""
    gui_script_path = project_root / "offjournal_gui" / "run_gui.py"
    if not gui_script_path.exists():
        print("Erro: O script da GUI 'offjournal_gui/run_gui.py' não foi encontrado.", file=sys.stderr)
        sys.exit(1)
    
    print("Iniciando a interface gráfica...")
    try:
        subprocess.run([sys.executable, str(gui_script_path)], check=True)
    except FileNotFoundError:
        print("Erro: O interpretador Python não foi encontrado. Verifique sua instalação.", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"\nA interface gráfica encontrou um erro e foi fechada (código de saída: {e.returncode}).", file=sys.stderr)
        print("Verifique se as dependências da GUI estão instaladas (veja README.md).", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nInterface gráfica fechada pelo usuário.")

if __name__ == "__main__":
    main_cli()
--- END OF FILE: offjournal/main.py ---

--- START OF FILE: offjournal/requirements.txt ---
# Este arquivo lista as dependências Python do projeto.
# Atualmente, o projeto offjournal não possui dependências externas
# que precisam ser instaladas via `pip`.

# A biblioteca `pydantic` é uma candidata para validação de dados
# no futuro, mas ainda não é uma dependência obrigatória.
# pydantic

# -------------------------------------------------------------------
# DEPENDÊNCIAS DA INTERFACE GRÁFICA (GUI)
# -------------------------------------------------------------------
#
# A interface gráfica (GUI) do off.journal requer bibliotecas do
# sistema que NÃO são instaladas com `pip install -r requirements.txt`.
#
# Você deve instalá-las usando o gerenciador de pacotes da sua
# distribuição Linux.
#
# --- Instruções de Instalação por Sistema ---
#
# Para Debian, Ubuntu e derivados:
# sudo apt update
# sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
#
# Para Arch Linux e derivados:
# sudo pacman -Syu python-gobject webkit2gtk
#
# Para Fedora, CentOS, RHEL:
# sudo dnf install python3-gobject webkit2gtk4.0
#
--- END OF FILE: offjournal/requirements.txt ---

--- START OF FILE: offjournal/LICENSE ---
(Conteúdo completo da licença GPLv3 aqui, como no arquivo original)
--- END OF FILE: offjournal/LICENSE ---

--- START OF FILE: offjournal/core/__init__.py ---
# core/__init__.py
"""
Core package initialization for offjournal.

This file makes it easier to import modules from the core package.
"""
from . import entry
from . import planner
from . import mood
from . import crypto
from . import export
from . import media
from . import utils
--- END OF FILE: offjournal/core/__init__.py ---

--- START OF FILE: offjournal/core/entry.py ---
# core/entry.py
"""
Entry management module for offjournal.

Provides functionality to create, edit, list, and manage journal entries.
All functions are designed to return structured data (lists or dicts)
to be used by any frontend (CLI, GUI, etc.).
"""
import os
from datetime import datetime
from pathlib import Path

# Base directory for all journal entries
ENTRIES_DIR = Path.home() / ".offjournal" / "entries"
ENTRIES_DIR.mkdir(parents=True, exist_ok=True)


def _parse_filename(path: Path) -> dict:
    """
    Extracts structured data (id, title) from a filename.
    Example: "20250715100000_My_First_Entry.md" ->
             {"id": "20250715100000", "title": "My First Entry"}
    """
    parts = path.stem.split('_', 1)
    return {
        "id": parts[0],
        "title": parts[1].replace('_', ' ') if len(parts) > 1 else "Sem Título",
        "filename": path.name
    }

def get_entries() -> list[dict]:
    """
    Returns a list of all journal entries, with newest first.
    Each entry is a dictionary containing its id, title, and filename.
    """
    try:
        files = sorted(ENTRIES_DIR.glob("*.md"), reverse=True)
        return [_parse_filename(f) for f in files]
    except OSError:
        return []

def find_entry_path(entry_id: str) -> Path | None:
    """
    Finds the full path of an entry by its ID prefix.
    Returns the Path object or None if not found.
    """
    if not entry_id or not entry_id.strip():
        return None
    
    # Use glob to find any file starting with the ID
    matches = list(ENTRIES_DIR.glob(f"{entry_id}*.md"))
    return matches[0] if matches else None

def get_entry_content(entry_id: str) -> str | None:
    """
    Returns the raw string content of a specific journal entry.
    Returns None if the entry is not found.
    """
    filepath = find_entry_path(entry_id)
    if not filepath:
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except IOError:
        return None

def update_entry_content(entry_id: str, new_content: str) -> dict:
    """
    Updates the content of an existing journal entry.
    Returns a dictionary with the status of the operation.
    """
    filepath = find_entry_path(entry_id)
    if not filepath:
        return {"status": "error", "message": "Entry not found."}

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return {"status": "success", "message": "Entrada salva com sucesso."}
    except IOError as e:
        return {"status": "error", "message": f"Falha ao escrever no arquivo: {e}"}

def create_entry(title: str) -> dict:
    """
    Creates a new journal entry and returns its data.
    Returns a dictionary with status and entry data or an error message.
    """
    if not title or not title.strip():
        return {"status": "error", "message": "O título não pode ser vazio."}

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_title = "_".join(title.strip().split())
    filename = f"{timestamp}_{safe_title}.md"
    filepath = ENTRIES_DIR / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title.strip()}\n\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Escreva seus pensamentos aqui...\n")
        
        return {
            "status": "success",
            "data": _parse_filename(filepath)
        }
    except IOError as e:
        return {"status": "error", "message": f"Falha ao criar a entrada: {e}"}

def delete_entry(entry_id: str) -> dict:
    """
    Deletes a journal entry by its ID.
    Returns a dictionary with the status of the operation.
    """
    filepath = find_entry_path(entry_id)
    if not filepath:
        return {"status": "error", "message": "Entrada não encontrada."}
    
    try:
        filepath.unlink()
        return {"status": "success", "message": "Entrada excluída com sucesso."}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao excluir a entrada: {e}"}
--- END OF FILE: offjournal/core/entry.py ---

--- START OF FILE: offjournal/core/planner.py ---
# core/planner.py
"""
Planner module for offjournal.

Manages an offline agenda with events stored in a JSON file.
All functions return structured data for consumption by any UI.
"""

import json
from pathlib import Path
from datetime import datetime

# Path to the planner data file
PLANNER_FILE = Path.home() / ".offjournal" / "planner.json"

def _load_events() -> list[dict]:
    """
    Loads events from the JSON file.
    Returns an empty list if the file doesn't exist or is invalid.
    """
    if not PLANNER_FILE.exists():
        return []
    try:
        with open(PLANNER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # In case of corruption or read error, treat as empty
        return []

def _save_events(events: list[dict]) -> bool:
    """
    Saves the list of events to the JSON file.
    Returns True on success, False on failure.
    """
    try:
        PLANNER_FILE.parent.mkdir(parents=True, exist_ok=True)
        # Sort by date before saving for consistency
        sorted_events = sorted(events, key=lambda x: (x.get('date', ''), x.get('id', 0)))
        with open(PLANNER_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted_events, f, indent=2)
        return True
    except IOError:
        return False

def get_events() -> list[dict]:
    """
    Returns all planner events, sorted by date.
    The list is returned directly as it's already structured data.
    """
    return _load_events()

def add_event(date_str: str, title: str) -> dict:
    """
    Adds a new event to the planner.
    Returns a dictionary with status and the newly created event data.
    """
    try:
        # Validate date format
        datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return {"status": "error", "message": "Formato de data inválido. Use AAAA-MM-DD."}
    
    if not title or not title.strip():
        return {"status": "error", "message": "O título do evento não pode ser vazio."}

    events = _load_events()
    new_id = max([ev.get("id", 0) for ev in events], default=0) + 1
    new_event = {"id": new_id, "date": date_str, "title": title.strip()}
    events.append(new_event)
    
    if _save_events(events):
        return {"status": "success", "data": new_event}
    else:
        return {"status": "error", "message": "Falha ao salvar o arquivo do planejador."}

def update_event(event_id: int, date_str: str | None = None, title: str | None = None) -> dict:
    """
    Updates an existing event's date and/or title.
    Returns a status dictionary.
    """
    if not isinstance(event_id, int):
        return {"status": "error", "message": "ID do evento inválido."}

    events = _load_events()
    event_found = False
    for ev in events:
        if ev.get("id") == event_id:
            event_found = True
            if date_str:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    ev["date"] = date_str
                except (ValueError, TypeError):
                    return {"status": "error", "message": "Formato de data inválido. Use AAAA-MM-DD."}
            if title:
                if not title.strip():
                    return {"status": "error", "message": "O título não pode ser vazio."}
                ev["title"] = title.strip()
            break
    
    if not event_found:
        return {"status": "error", "message": f"Evento com ID {event_id} não encontrado."}
    
    if _save_events(events):
        return {"status": "success", "message": f"Evento {event_id} atualizado com sucesso."}
    else:
        return {"status": "error", "message": "Falha ao salvar o arquivo do planejador."}

def delete_event(event_id: int) -> dict:
    """
    Deletes an event from the planner by its ID.
    Returns a status dictionary.
    """
    if not isinstance(event_id, int):
        return {"status": "error", "message": "ID do evento inválido."}

    events = _load_events()
    initial_count = len(events)
    filtered_events = [ev for ev in events if ev.get("id") != event_id]
    
    if len(filtered_events) == initial_count:
        return {"status": "error", "message": f"Evento com ID {event_id} não encontrado."}

    if _save_events(filtered_events):
        return {"status": "success", "message": f"Evento {event_id} removido com sucesso."}
    else:
        return {"status": "error", "message": "Falha ao salvar o arquivo do planejador."}
--- END OF FILE: offjournal/core/planner.py ---

--- START OF FILE: offjournal/core/crypto.py ---
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
--- END OF FILE: offjournal/core/crypto.py ---

--- START OF FILE: offjournal/core/export.py ---
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
--- END OF FILE: offjournal/core/export.py ---

--- START OF FILE: offjournal/core/media.py ---
# core/media.py
"""
Media management module for offjournal.

Handles adding, listing, and removing media attachments linked to journal entries.
All functions return structured data.
"""

import shutil
from pathlib import Path

# Base directory for all media attachments, organized by entry ID
MEDIA_DIR = Path.home() / ".offjournal" / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

def add_media(entry_id: str, media_path_str: str) -> dict:
    """
    Adds a media file as an attachment to a journal entry.

    Args:
        entry_id (str): Identifier of the journal entry.
        media_path_str (str): Path to the media file to attach.

    Returns:
        dict: A status dictionary.
    """
    media_file = Path(media_path_str)
    if not media_file.exists():
        return {"status": "error", "message": f"Arquivo de mídia não existe: {media_path_str}"}

    if not entry_id:
        return {"status": "error", "message": "ID da entrada não pode ser vazio."}

    try:
        dest_dir = MEDIA_DIR / entry_id
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / media_file.name
        if dest_file.exists():
            return {"status": "error", "message": f"Arquivo de mídia '{media_file.name}' já existe para esta entrada."}

        shutil.copy2(media_file, dest_file)
        return {"status": "success", "message": f"Mídia '{media_file.name}' adicionada à entrada '{entry_id}'."}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao adicionar mídia: {e}"}

def list_media(entry_id: str) -> dict:
    """
    Lists all media attachments for a journal entry.

    Args:
        entry_id (str): Identifier of the journal entry.

    Returns:
        dict: A status dictionary containing a list of filenames on success.
    """
    if not entry_id:
        return {"status": "error", "message": "ID da entrada não pode ser vazio."}

    media_folder = MEDIA_DIR / entry_id
    if not media_folder.is_dir():
        # It's not an error if a folder doesn't exist, just means no media
        return {"status": "success", "data": []}

    try:
        files = [f.name for f in media_folder.iterdir() if f.is_file()]
        return {"status": "success", "data": sorted(files)}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao listar mídias: {e}"}

def remove_media(entry_id: str, media_filename: str) -> dict:
    """
    Removes a specific media attachment from a journal entry.

    Args:
        entry_id (str): Identifier of the journal entry.
        media_filename (str): Name of the media file to remove.

    Returns:
        dict: A status dictionary.
    """
    if not entry_id or not media_filename:
        return {"status": "error", "message": "ID da entrada e nome da mídia não podem ser vazios."}

    media_file = MEDIA_DIR / entry_id / media_filename
    if not media_file.exists():
        return {"status": "error", "message": f"Arquivo de mídia '{media_filename}' não encontrado para a entrada '{entry_id}'."}

    try:
        media_file.unlink()
        return {"status": "success", "message": f"Mídia '{media_filename}' removida com sucesso."}
    except OSError as e:
        return {"status": "error", "message": f"Falha ao remover mídia: {e}"}
--- END OF FILE: offjournal/core/media.py ---

--- START OF FILE: offjournal/core/mood.py ---
# core/mood.py
"""
Mood analysis module for offjournal.

Provides a simple sentiment analysis of journal entries based on keyword matching.
"""

from pathlib import Path

# This should point to the same directory as in core/entry.py
ENTRIES_DIR = Path.home() / ".offjournal" / "entries"

# Simple word lists for positive and negative sentiment
# (in Portuguese, to match potential user input)
POSITIVE_WORDS = {"feliz", "alegre", "amor", "animado", "ótimo", "bom", "incrível", "fantástico", "sucesso", "grato", "orgulhoso"}
NEGATIVE_WORDS = {"triste", "raiva", "chateado", "ruim", "péssimo", "ódio", "deprimido", "terrível", "frustrado", "medo", "ansioso"}

def _find_entry_path(entry_id: str) -> Path | None:
    """Helper to find an entry path by its ID. Avoids code duplication."""
    if not entry_id or not entry_id.strip():
        return None
    matches = list(ENTRIES_DIR.glob(f"{entry_id}*.md"))
    return matches[0] if matches else None

def analyze_entry_mood(entry_id: str) -> dict:
    """
    Analyzes the mood of a specific journal entry.

    Args:
        entry_id (str): The ID (timestamp prefix) of the entry to analyze.

    Returns:
        A dictionary with the mood analysis results or an error.
        Example: {"status": "success", "mood": "Positive", "positive": 5, "negative": 1}
    """
    filepath = _find_entry_path(entry_id)
    if not filepath:
        return {"status": "error", "message": f"Entrada '{entry_id}' não encontrada."}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # Normalize text to lowercase for case-insensitive matching
            text = f.read().lower()

        positive_count = sum(word in text for word in POSITIVE_WORDS)
        negative_count = sum(word in text for word in NEGATIVE_WORDS)

        mood = "Neutro"
        if positive_count > negative_count:
            mood = "Positivo"
        elif negative_count > positive_count:
            mood = "Negativo"

        return {
            "status": "success",
            "entry_id": entry_id,
            "filename": filepath.name,
            "mood": mood,
            "positive_score": positive_count,
            "negative_score": negative_count
        }
    except IOError as e:
        return {"status": "error", "message": f"Não foi possível ler o arquivo da entrada: {e}"}
--- END OF FILE: offjournal/core/mood.py ---

--- START OF FILE: offjournal/core/utils.py ---
# core/utils.py
"""
Utility functions for offjournal.
Provides generic helper functions to support other modules.
"""
from pathlib import Path
from datetime import datetime

def ensure_dir(path: str) -> None:
    """Ensures a directory exists, creating it if necessary."""
    Path(path).mkdir(parents=True, exist_ok=True)

def read_file(filepath: str) -> str:
    """Reads the content of a text file."""
    return Path(filepath).read_text(encoding="utf-8")

def write_file(filepath: str, content: str) -> None:
    """Writes content to a text file, overwriting if it exists."""
    Path(filepath).write_text(content, encoding="utf-8")

def get_current_timestamp(fmt: str = "%Y%m%d%H%M%S") -> str:
    """Returns the current timestamp as a formatted string."""
    return datetime.now().strftime(fmt)

def validate_non_empty_string(s: str) -> bool:
    """Validates if a string is non-empty and not just whitespace."""
    return bool(s and s.strip())
--- END OF FILE: offjournal/core/utils.py ---

--- START OF FILE: offjournal/offjournal_gui/run_gui.py ---
#!/usr/bin/env python3
# offjournal_gui/run_gui.py

"""
Main entry point for the off.journal GUI application.

This script initializes a GTK window, embeds a WebKitWebView,
and sets up a communication bridge between the Python backend (core)
and the JavaScript frontend.
"""

import gi
import json
import sys
from pathlib import Path

# Add the project root directory to sys.path
# This allows us to import the 'core' package from anywhere.
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from core import entry, planner

# Check for GTK and WebKit dependencies
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('WebKit2', '4.0')
    from gi.repository import Gtk, WebKit2
except (ValueError, ImportError):
    print("Erro: Dependências da GUI não encontradas.", file=sys.stderr)
    print("Por favor, instale PyGObject e WebKit2GTK para sua distribuição.", file=sys.stderr)
    print("Ex (Debian/Ubuntu): sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.0", file=sys.stderr)
    sys.exit(1)


class App:
    """The main application class for the GUI."""
    def __init__(self):
        self.window = Gtk.Window(title="off.journal")
        self.window.set_default_size(950, 700)
        self.window.connect("destroy", Gtk.main_quit)

        # Set up the communication bridge between JS and Python
        self.manager = WebKit2.UserContentManager()
        self.manager.register_script_message_handler("bridge")
        self.manager.connect("script-message-received::bridge", self.on_js_message)

        self.webview = WebKit2.WebView.new_with_user_content_manager(self.manager)
        
        # Enable the developer inspector for debugging (Right-click -> Inspect Element)
        settings = self.webview.get_settings()
        settings.set_enable_developer_extras(True)

        # Load the frontend HTML file
        frontend_path = project_root / "offjournal_gui" / "frontend" / "index.html"
        if not frontend_path.exists():
             self.show_error_dialog("Arquivo de Interface Não Encontrado", 
                                    f"Não foi possível encontrar o arquivo:\n{frontend_path}")
             sys.exit(1)
        self.webview.load_uri(frontend_path.as_uri())

        self.window.add(self.webview)
        self.window.show_all()

    def send_to_js(self, data: dict):
        """Helper function to send a JSON response to the JavaScript frontend."""
        try:
            js_code = f"window.handlePythonResponse({json.dumps(data)});"
            self.webview.run_javascript(js_code)
        except Exception as e:
            print(f"Error sending data to JS: {e}", file=sys.stderr)

    def on_js_message(self, manager, message):
        """
        Handles incoming messages from the JavaScript frontend.
        This acts as a router, mapping commands to core backend functions.
        """
        try:
            req = json.loads(message.get_js_value().to_string())
            command = req.get("command")
            payload = req.get("payload", {})
            
            if not command:
                self.send_to_js({"status": "error", "message": "Comando ausente na requisição."})
                return

            # --- Command Router ---
            response_data = None
            if command == "entries:list":
                response_data = entry.get_entries()
            elif command == "entries:get_content":
                response_data = entry.get_entry_content(payload.get("id"))
            elif command == "entries:update":
                response_data = entry.update_entry_content(payload.get("id"), payload.get("content"))
            elif command == "entries:create":
                response_data = entry.create_entry(payload.get("title"))
            elif command == "entries:delete":
                response_data = entry.delete_entry(payload.get("id"))
            elif command == "planner:list":
                response_data = planner.get_events()
            elif command == "planner:add":
                response_data = planner.add_event(payload.get("date"), payload.get("title"))
            elif command == "planner:delete":
                response_data = planner.delete_event(payload.get("id"))
            else:
                 self.send_to_js({
                     "status": "error", 
                     "command": command, 
                     "message": "Comando desconhecido pelo backend."
                })
                 return

            # Send a successful response back to the frontend
            self.send_to_js({"status": "success", "command": command, "data": response_data})

        except Exception as e:
            print(f"Backend Error on command '{command}': {e}", file=sys.stderr)
            self.send_to_js({"status": "error", "command": command, "message": f"Erro interno no backend: {str(e)}"})

    def show_error_dialog(self, title, text):
        """Displays a GTK error dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

def run():
    """Initializes and runs the GTK application."""
    app = App()
    Gtk.main()

if __name__ == "__main__":
    run()
--- END OF FILE: offjournal/offjournal_gui/run_gui.py ---

--- START OF FILE: offjournal/offjournal_gui/frontend/index.html ---
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>off.journal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Barra Lateral de Navegação -->
        <aside class="sidebar">
            <header>
                <h1>off.journal</h1>
            </header>
            <nav>
                <ul>
                    <li><button id="nav-diary" class="nav-button active" title="Ver entradas do diário">Diário</button></li>
                    <li><button id="nav-planner" class="nav-button" title="Acessar o planejador">Planejador</button></li>
                </ul>
            </nav>
        </aside>

        <!-- Conteúdo Principal -->
        <main class="main-content">

            <!-- Visão do Diário -->
            <div id="diary-view" class="view active-view">
                <!-- Painel com a Lista de Entradas -->
                <div class="content-list-pane">
                    <div class="pane-header">
                        <h2>Entradas</h2>
                        <button id="btn-new-entry" class="btn-primary" title="Criar uma nova entrada no diário">+ Nova Entrada</button>
                    </div>
                    <ul id="entry-list" class="item-list">
                        <!-- Entradas do diário serão injetadas aqui pelo script.js -->
                    </ul>
                </div>
                <!-- Painel com o Detalhe/Editor da Entrada -->
                <div class="content-detail-pane">
                    <div id="entry-viewer" class="viewer">
                        <!-- Mensagem de Boas-Vindas (quando nada está selecionado) -->
                        <div id="entry-welcome" class="welcome-message">
                            <p>Selecione uma entrada para ler ou editar.</p>
                            <p>Ou crie uma nova entrada no diário.</p>
                        </div>
                        <!-- Editor de Texto (visível quando uma entrada é selecionada) -->
                        <div id="entry-editor" class="editor" style="display: none;">
                            <textarea id="editor-textarea" placeholder="Escreva aqui..."></textarea>
                            <div class="editor-actions">
                                <button id="btn-save-entry" class="btn-primary" title="Salvar as alterações (Ctrl+S)">Salvar</button>
                                <span id="save-status"></span>
                                <button id="btn-delete-entry" class="btn-danger" title="Excluir esta entrada permanentemente">Excluir</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Visão do Planejador -->
            <div id="planner-view" class="view">
                <div class="planner-container">
                    <div class="pane-header">
                        <h2>Planejador</h2>
                    </div>
                    <div class="add-event-form">
                        <h3>Adicionar Novo Evento</h3>
                        <input type="date" id="planner-date" title="Data do evento">
                        <input type="text" id="planner-title" placeholder="Descrição do evento" title="Título do evento">
                        <button id="btn-add-event" class="btn-primary">Adicionar</button>
                    </div>
                    <div class="event-list-container">
                        <h3>Próximos Eventos</h3>
                        <ul id="event-list" class="item-list">
                            <!-- Eventos serão injetados aqui pelo script.js -->
                        </ul>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <!-- O script que controla toda a lógica da interface -->
    <script src="script.js"></script>
</body>
</html>
--- END OF FILE: offjournal/offjournal_gui/frontend/index.html ---

--- START OF FILE: offjournal/offjournal_gui/frontend/style.css ---
/* --- Variaveis de Cor e Fontes (Tema Escuro) --- */
:root {
    --bg-darker: #21252b;
    --bg-dark: #282c34;
    --bg-medium: #3a3f4b;
    --bg-light: #4b5263;
    --text-primary: #abb2bf;
    --text-secondary: #828997;
    --accent-color: #61afef;
    --accent-color-hover: #7BC3FF;
    --danger-color: #e06c75;
    --danger-color-hover: #ff7b86;
    --success-color: #98c379;
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    --font-mono: "Fira Code", "Source Code Pro", Menlo, Monaco, Consolas, "Courier New", monospace;
}

/* --- Reset e Estilos Globais --- */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: var(--font-family);
    background-color: var(--bg-dark);
    color: var(--text-primary);
    overflow: hidden;
    height: 100vh;
    width: 100vw;
    font-size: 16px;
}

.container {
    display: flex;
    height: 100%;
}

/* --- Barra Lateral (Sidebar) --- */
.sidebar {
    width: 220px;
    background-color: var(--bg-darker);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
}

.sidebar header h1 {
    font-size: 1.5rem;
    text-align: center;
    margin-bottom: 2rem;
    color: white;
}

.sidebar nav ul {
    list-style-type: none;
}

.nav-button {
    width: 100%;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    background-color: transparent;
    border: none;
    color: var(--text-secondary);
    text-align: left;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.nav-button:hover {
    background-color: var(--bg-medium);
    color: white;
}

.nav-button.active {
    background-color: var(--accent-color);
    color: white;
    font-weight: 600;
}

/* --- Conteúdo Principal e Vistas (Views) --- */
.main-content {
    flex-grow: 1;
    display: flex;
}

.view {
    display: none;
    width: 100%;
    height: 100%;
}

.view.active-view {
    display: flex;
}

/* --- Painéis da Vista do Diário --- */
.content-list-pane {
    width: 320px;
    border-right: 1px solid var(--bg-darker);
    display: flex;
    flex-direction: column;
    height: 100vh;
    flex-shrink: 0;
}

.pane-header {
    padding: 1rem;
    border-bottom: 1px solid var(--bg-darker);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
}

.pane-header h2 {
    color: white;
}

.content-detail-pane {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

/* --- Listas de Itens (Entradas e Eventos) --- */
.item-list {
    list-style: none;
    overflow-y: auto;
    flex-grow: 1;
}

.item-list li {
    padding: 1rem;
    cursor: pointer;
    border-bottom: 1px solid var(--bg-dark);
    transition: background-color 0.2s;
}

.item-list li:hover {
    background-color: var(--bg-medium);
}

.item-list li.selected {
    background-color: var(--accent-color);
    color: white;
}
.item-list li.selected .item-subtitle {
    color: #e0e0e0;
}


.item-list .item-title {
    font-weight: bold;
    display: block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 0.25rem;
}

.item-list .item-subtitle {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-family: var(--font-mono);
}

.item-list .empty-list {
    padding: 2rem 1rem;
    text-align: center;
    color: var(--text-secondary);
    cursor: default;
}

/* --- Editor de Entrada --- */
.viewer {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.welcome-message {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: var(--text-secondary);
    text-align: center;
    padding: 2rem;
}

.editor {
    height: 100%;
    display: flex;
    flex-direction: column;
}

#editor-textarea {
    flex-grow: 1;
    width: 100%;
    background-color: var(--bg-dark);
    color: var(--text-primary);
    border: none;
    padding: 1.5rem;
    font-size: 1.05rem;
    line-height: 1.7;
    resize: none;
    font-family: var(--font-mono);
}

#editor-textarea:focus {
    outline: none;
}

.editor-actions {
    padding: 0.75rem 1.5rem;
    border-top: 1px solid var(--bg-darker);
    display: flex;
    align-items: center;
    background-color: var(--bg-darker);
}

#save-status {
    margin-left: 1rem;
    font-size: 0.9rem;
    color: var(--text-secondary);
    transition: color 0.3s;
}

/* --- Vista do Planejador --- */
#planner-view {
    padding: 1rem 2rem;
    overflow-y: auto;
    width: 100%;
    display: block; /* Sobrescreve o flex para permitir rolagem vertical */
}

.planner-container {
    max-width: 800px;
    margin: 0 auto;
}

.add-event-form {
    background-color: var(--bg-darker);
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0 2rem 0;
    display: flex;
    gap: 1rem;
    align-items: center;
}
.add-event-form h3 {
    margin: 0;
    margin-right: auto;
    color: white;
}

.event-list-container h3 {
    margin-bottom: 1rem;
    color: white;
}
#event-list .item-list-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
#event-list .event-date {
    font-weight: bold;
    font-family: var(--font-mono);
    background-color: var(--bg-light);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    margin-right: 1rem;
    color: white;
}
#event-list .event-title {
    flex-grow: 1;
}

/* --- Botões e Inputs --- */
.btn-primary, .btn-danger {
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
}

.btn-primary {
    background-color: var(--accent-color);
    color: white;
}
.btn-primary:hover {
    background-color: var(--accent-color-hover);
}

.btn-danger {
    margin-left: auto;
    background-color: var(--danger-color);
    color: white;
}
.btn-danger:hover {
    background-color: var(--danger-color-hover);
}

#planner-date, #planner-title {
    padding: 0.6rem;
    border-radius: 5px;
    border: 1px solid var(--bg-light);
    background-color: var(--bg-dark);
    color: var(--text-primary);
    font-size: 1rem;
}

.btn-delete-event {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 1.4rem;
    padding: 0 0.5rem;
}
.btn-delete-event:hover {
    color: var(--danger-color);
}
--- END OF FILE: offjournal/offjournal_gui/frontend/style.css ---

--- START OF FILE: offjournal/offjournal_gui/frontend/script.js ---
document.addEventListener('DOMContentLoaded', () => {
    // --- State Management ---
    let state = {
        currentView: 'diary',
        currentEntryId: null,
        isDirty: false, // Flag to check if the editor has unsaved changes
    };

    // --- Debounce for saving ---
    let saveTimeout = null;
    let statusTimeout = null;

    // --- DOM Elements ---
    const elements = {
        views: {
            diary: document.getElementById('diary-view'),
            planner: document.getElementById('planner-view'),
        },
        navButtons: {
            diary: document.getElementById('nav-diary'),
            planner: document.getElementById('nav-planner'),
        },
        entryList: document.getElementById('entry-list'),
        eventList: document.getElementById('event-list'),
        entryWelcome: document.getElementById('entry-welcome'),
        entryEditor: document.getElementById('entry-editor'),
        editorTextarea: document.getElementById('editor-textarea'),
        saveStatus: document.getElementById('save-status'),
        btnSaveEntry: document.getElementById('btn-save-entry'),
        btnDeleteEntry: document.getElementById('btn-delete-entry'),
        btnNewEntry: document.getElementById('btn-new-entry'),
        btnAddEvent: document.getElementById('btn-add-event'),
        plannerDate: document.getElementById('planner-date'),
        plannerTitle: document.getElementById('planner-title'),
    };

    // --- API Communication Layer ---
    const api = {
        send: (command, payload = {}) => {
            try {
                window.webkit.messageHandlers.bridge.postMessage(JSON.stringify({ command, payload }));
            } catch (error) {
                console.error("Falha na comunicação com o backend Python. A aplicação está sendo executada no modo GUI?", error);
                alert("Erro de comunicação: Não foi possível contatar o backend.");
            }
        },
        entries: {
            list: () => api.send('entries:list'),
            getContent: (id) => api.send('entries:get_content', { id }),
            update: (id, content) => api.send('entries:update', { id, content }),
            create: (title) => api.send('entries:create', { title }),
            delete: (id) => api.send('entries:delete', { id }),
        },
        planner: {
            list: () => api.send('planner:list'),
            add: (date, title) => api.send('planner:add', {date, title}),
            delete: (id) => api.send('planner:delete', {id}),
        }
    };

    // --- UI Rendering ---
    const ui = {
        switchView(viewName) {
            state.currentView = viewName;
            Object.values(elements.views).forEach(v => v.classList.remove('active-view'));
            Object.values(elements.navButtons).forEach(b => b.classList.remove('active'));
            elements.views[viewName].classList.add('active-view');
            elements.navButtons[viewName].classList.add('active');

            if (viewName === 'diary') api.entries.list();
            if (viewName === 'planner') api.planner.list();
        },
        renderEntryList(entries) {
            elements.entryList.innerHTML = '';
            if (!entries || entries.length === 0) {
                elements.entryList.innerHTML = '<li class="empty-list">Nenhuma entrada encontrada.</li>';
                return;
            }
            entries.forEach(entry => {
                const li = document.createElement('li');
                li.dataset.id = entry.id;
                li.className = (entry.id === state.currentEntryId) ? 'selected' : '';
                li.innerHTML = `
                    <span class="item-title">${entry.title}</span>
                    <span class="item-subtitle">${entry.id}</span>
                `;
                li.addEventListener('click', () => handlers.selectEntry(entry.id));
                elements.entryList.appendChild(li);
            });
        },
        renderEventList(events) {
            elements.eventList.innerHTML = '';
             if (!events || events.length === 0) {
                elements.eventList.innerHTML = '<li class="empty-list">Nenhum evento no planejador.</li>';
                return;
            }
            events.forEach(event => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="item-list-row">
                        <span class="event-date">${event.date}</span>
                        <span class="event-title">${event.title}</span>
                        <button class="btn-delete-event" data-id="${event.id}" title="Excluir evento">&times;</button>
                    </div>
                `;
                li.querySelector('.btn-delete-event').addEventListener('click', (e) => {
                    e.stopPropagation();
                    handlers.deleteEvent(event.id, event.title);
                });
                elements.eventList.appendChild(li);
            });
        },
        showEditor(content) {
            elements.entryWelcome.style.display = 'none';
            elements.entryEditor.style.display = 'flex';
            elements.editorTextarea.value = content;
            elements.editorTextarea.focus();
            state.isDirty = false;
        },
        showWelcome() {
            elements.entryWelcome.style.display = 'flex';
            elements.entryEditor.style.display = 'none';
            state.currentEntryId = null;
            state.isDirty = false;
            document.querySelectorAll('#entry-list li').forEach(item => item.classList.remove('selected'));
        },
        updateSaveStatus(message, isError = false) {
            elements.saveStatus.textContent = message;
            elements.saveStatus.style.color = isError ? 'var(--danger-color)' : 'var(--text-secondary)';
            clearTimeout(statusTimeout);
            statusTimeout = setTimeout(() => elements.saveStatus.textContent = '', 3000);
        }
    };

    // --- Event Handlers & Logic ---
    const handlers = {
        selectEntry(id) {
            if (state.isDirty && !confirm("Você tem alterações não salvas. Deseja descartá-las?")) {
                return;
            }
            state.currentEntryId = id;
            api.entries.getContent(id);
            document.querySelectorAll('#entry-list li').forEach(item => item.classList.remove('selected'));
            document.querySelector(`#entry-list li[data-id='${id}']`)?.classList.add('selected');
        },
        saveCurrentEntry() {
            if (state.currentEntryId) {
                api.entries.update(state.currentEntryId, elements.editorTextarea.value);
                state.isDirty = false;
            }
        },
        onEditorInput() {
            state.isDirty = true;
            ui.updateSaveStatus('Alterações não salvas...');
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(handlers.saveCurrentEntry, 2000); // Auto-save after 2 seconds of inactivity
        },
        createNewEntry() {
            const title = prompt("Digite o título para a nova entrada:", "Nova Entrada");
            if (title && title.trim()) {
                api.entries.create(title);
            }
        },
        deleteCurrentEntry() {
            if (state.currentEntryId && confirm("Tem certeza que deseja excluir esta entrada? A ação não pode ser desfeita.")) {
                api.entries.delete(state.currentEntryId);
            }
        },
        addNewEvent() {
            const date = elements.plannerDate.value;
            const title = elements.plannerTitle.value;
            if (date && title.trim()) {
                api.planner.add(date, title);
            } else {
                alert("Por favor, preencha a data e o título do evento.");
            }
        },
        deleteEvent(id, title) {
            if (confirm(`Tem certeza que deseja excluir o evento "${title}"?`)) {
                api.planner.delete(id);
            }
        },
        handleKeyDown(e) {
            // Salvar com Ctrl+S
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                clearTimeout(saveTimeout); // Prevent auto-save from firing
                handlers.saveCurrentEntry();
            }
        }
    };

    // --- Python Response Handler ---
    window.handlePythonResponse = (response) => {
        console.log('Received from Python:', response);
        const { status, command, data, message } = response;

        if (status === 'error') {
            alert(`Erro: ${message}`);
            return;
        }

        switch (command) {
            case 'entries:list':
                ui.renderEntryList(data);
                break;
            case 'entries:get_content':
                ui.showEditor(data);
                break;
            case 'entries:update':
                if (data.status === 'success') {
                    ui.updateSaveStatus(data.message);
                } else {
                    ui.updateSaveStatus(data.message, true);
                }
                break;
            case 'entries:create':
                state.currentEntryId = data.data.id;
                api.entries.list(); // Refresh list
                handlers.selectEntry(state.currentEntryId);
                break;
            case 'entries:delete':
                ui.showWelcome();
                api.entries.list(); // Refresh list
                break;
            case 'planner:list':
                ui.renderEventList(data);
                break;
            case 'planner:add':
            case 'planner:delete':
                 api.planner.list(); // Refresh list on add/delete
                 if (command === 'planner:add' && data.status === 'success') {
                     elements.plannerTitle.value = '';
                     elements.plannerTitle.focus();
                 }
                break;
        }
    };

    // --- Initialize ---
    const init = () => {
        // Setup event listeners
        elements.navButtons.diary.addEventListener('click', () => ui.switchView('diary'));
        elements.navButtons.planner.addEventListener('click', () => ui.switchView('planner'));
        elements.btnNewEntry.addEventListener('click', handlers.createNewEntry);
        elements.btnSaveEntry.addEventListener('click', handlers.saveCurrentEntry);
        elements.btnDeleteEntry.addEventListener('click', handlers.deleteCurrentEntry);
        elements.btnAddEvent.addEventListener('click', handlers.addNewEvent);
        elements.editorTextarea.addEventListener('input', handlers.onEditorInput);
        document.addEventListener('keydown', handlers.handleKeyDown);

        // Set planner date to today and load initial view
        elements.plannerDate.value = new Date().toISOString().split('T')[0];
        ui.switchView('diary');
    };

    init();
});
--- END OF FILE: offjournal/offjournal_gui/frontend/script.js ---

--- START OF FILE: offjournal/tests/test_crypto.py ---
# tests/test_crypto.py

import unittest
import tempfile
import shutil
from pathlib import Path
import core.crypto as crypto

# Helper to check if gpg command exists
def is_gpg_available():
    return shutil.which("gpg") is not None

class TestCryptoModule(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test.txt"
        self.test_file.write_text("This is a test file for crypto.", encoding="utf-8")
        
        # NOTE: For a real CI/CD environment, you'd need a dedicated, passwordless GPG key.
        # For local testing, this recipient should be a valid key ID in your GPG keyring.
        # If you don't have one, this test will likely fail on the encryption step.
        # We'll use a placeholder email.
        self.recipient = "test@example.com"

    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_encrypt_file_not_exist(self):
        """Test that encrypting a non-existent file returns an error status."""
        result = crypto.encrypt_file("nonexistent_file.txt", self.recipient)
        self.assertEqual(result["status"], "error")
        self.assertIn("Arquivo não encontrado", result["message"])

    def test_decrypt_non_gpg_file(self):
        """Test that decrypting a file without a .gpg extension returns an error."""
        result = crypto.decrypt_file(str(self.test_file))
        self.assertEqual(result["status"], "error")
        self.assertIn("não tem a extensão .gpg", result["message"])

    def test_decrypt_non_existent_file(self):
        """Test that decrypting a non-existent file returns an error."""
        result = crypto.decrypt_file("nonexistent_file.txt.gpg")
        self.assertEqual(result["status"], "error")
        self.assertIn("Arquivo não encontrado", result["message"])

    @unittest.skipUnless(is_gpg_available(), "GnuPG (gpg) command not found in PATH, skipping test.")
    def test_encrypt_with_invalid_recipient(self):
        """Test encryption with a recipient that does not exist in the keyring."""
        # Using a clearly invalid recipient
        invalid_recipient = "nobody@invalid-domain-12345.xyz"
        result = crypto.encrypt_file(str(self.test_file), invalid_recipient)
        
        self.assertEqual(result["status"], "error")
        # GPG's error message for a missing key usually contains "No public key"
        self.assertIn("public key", result["message"].lower())

    # This is an integration test and requires a valid GPG setup.
    # It might fail if a valid key for self.recipient is not available.
    @unittest.skipUnless(is_gpg_available(), "GnuPG (gpg) command not found in PATH, skipping test.")
    @unittest.skip("Skipping GPG cycle test by default as it requires a valid local key.")
    def test_encrypt_decrypt_cycle(self):
        """
        Test the full encrypt-decrypt cycle.
        
        NOTE: This test requires a GPG key for 'test@example.com' (or your email)
        to be present in your local GPG keyring.
        """
        # Encrypt the file
        encrypt_result = crypto.encrypt_file(str(self.test_file), self.recipient)
        self.assertEqual(encrypt_result["status"], "success", f"Encryption failed: {encrypt_result.get('message')}")
        
        encrypted_file_path = Path(encrypt_result["output_path"])
        self.assertTrue(encrypted_file_path.exists())

        # Original file can be removed to ensure decryption works from scratch
        self.test_file.unlink()
        self.assertFalse(self.test_file.exists())

        # Decrypt the file
        decrypt_result = crypto.decrypt_file(str(encrypted_file_path))
        self.assertEqual(decrypt_result["status"], "success", f"Decryption failed: {decrypt_result.get('message')}")
        
        decrypted_file_path = Path(decrypt_result["output_path"])
        self.assertTrue(decrypted_file_path.exists())
        
        # Verify content
        decrypted_content = decrypted_file_path.read_text(encoding="utf-8")
        self.assertEqual(decrypted_content, "This is a test file for crypto.")
--- END OF FILE: offjournal/tests/test_crypto.py ---

--- START OF FILE: offjournal/tests/test_entry.py ---
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

    def test_create_entry_success(self):
        """Test successful creation of a new entry."""
        title = "My First Test Entry"
        result = entry.create_entry(title)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        
        entry_data = result["data"]
        self.assertEqual(entry_data["title"], title)
        
        filepath = entry.ENTRIES_DIR / entry_data["filename"]
        self.assertTrue(filepath.exists())
        self.assertIn(f"# {title}", filepath.read_text())

    def test_create_entry_empty_title(self):
        """Test that creating an entry with an empty title fails."""
        result = entry.create_entry("   ")
        self.assertEqual(result["status"], "error")
        self.assertIn("título não pode ser vazio", result["message"])

    def test_get_entries(self):
        """Test listing of multiple entries."""
        self.assertEqual(entry.get_entries(), [])

        entry.create_entry("Entry One")
        entry.create_entry("Entry Two")

        entries = entry.get_entries()
        self.assertEqual(len(entries), 2)
        
        self.assertEqual(entries[0]["title"], "Entry Two")
        self.assertEqual(entries[1]["title"], "Entry One")

    def test_get_and_update_content(self):
        """Test the full cycle of getting, updating, and re-getting content."""
        create_result = entry.create_entry("Content Test")
        entry_id = create_result["data"]["id"]

        initial_content = entry.get_entry_content(entry_id)
        self.assertIn("# Content Test", initial_content)

        new_content = "# Updated Title\n\nThis is the new content."
        update_result = entry.update_entry_content(entry_id, new_content)
        self.assertEqual(update_result["status"], "success")

        updated_content = entry.get_entry_content(entry_id)
        self.assertEqual(updated_content, new_content)

    def test_delete_entry(self):
        """Test deleting an entry."""
        create_result = entry.create_entry("To Be Deleted")
        entry_id = create_result["data"]["id"]

        self.assertEqual(len(entry.get_entries()), 1)

        delete_result = entry.delete_entry(entry_id)
        self.assertEqual(delete_result["status"], "success")

        self.assertEqual(len(entry.get_entries()), 0)
        self.assertIsNone(entry.find_entry_path(entry_id))
--- END OF FILE: offjournal/tests/test_entry.py ---

--- START OF FILE: offjournal/tests/test_export.py ---
# tests/test_export.py

import unittest
import tempfile
import json
from pathlib import Path
import core.export as export

class TestExportModule(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory and a sample input file for each test."""
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_dir = Path(self.temp_dir_obj.name)
        
        self.input_file = self.temp_dir / "entry.md"
        self.test_content = "## Test Content\n\n- Point 1\n- Point 2"
        self.input_file.write_text(self.test_content, encoding="utf-8")

    def tearDown(self):
        """Clean up the temporary directory."""
        self.temp_dir_obj.cleanup()

    def test_export_to_txt_success(self):
        """Test successful export to a TXT file."""
        output_file = self.temp_dir / "output.txt"
        result = export.export_to_txt(str(self.input_file), str(output_file))
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(output_file.exists())
        self.assertEqual(output_file.read_text(encoding="utf-8"), self.test_content)

    def test_export_to_json_success(self):
        """Test successful export to a JSON file."""
        output_file = self.temp_dir / "output.json"
        result = export.export_to_json(str(self.input_file), str(output_file))
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(output_file.exists())
        
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data["source_filename"], "entry.md")
        self.assertEqual(data["content"], self.test_content)

    def test_export_input_file_not_found(self):
        """Test that exporting a non-existent file returns an error."""
        output_file = self.temp_dir / "output.txt"
        result = export.export_to_txt("non_existent_input.md", str(output_file))
        
        self.assertEqual(result["status"], "error")
        self.assertIn("Arquivo de entrada não encontrado", result["message"])
--- END OF FILE: offjournal/tests/test_export.py ---

--- START OF FILE: offjournal/tests/test_media.py ---
# tests/test_media.py

import unittest
import tempfile
import shutil
from pathlib import Path

import core.media as media

class TestMediaModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary directory for all media tests."""
        cls.test_base_dir = tempfile.mkdtemp(prefix="offjournal_media_test_")
        media.MEDIA_DIR = Path(cls.test_base_dir)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory after all tests."""
        shutil.rmtree(cls.test_base_dir)

    def setUp(self):
        """Create a dummy media file for each test."""
        self.entry_id = "20250715120000_test_entry"
        self.source_media_file = media.MEDIA_DIR / "source_image.jpg"
        self.source_media_file.write_text("dummy image content", encoding="utf-8")

    def tearDown(self):
        """Clean up the entry-specific media folder after each test."""
        entry_media_dir = media.MEDIA_DIR / self.entry_id
        if entry_media_dir.exists():
            shutil.rmtree(entry_media_dir)
        if self.source_media_file.exists():
            self.source_media_file.unlink()

    def test_add_media_success(self):
        """Test successfully adding a media file to an entry."""
        result = media.add_media(self.entry_id, str(self.source_media_file))
        self.assertEqual(result["status"], "success")
        
        dest_file = media.MEDIA_DIR / self.entry_id / self.source_media_file.name
        self.assertTrue(dest_file.exists())

    def test_list_and_remove_media(self):
        """Test listing and removing media for an entry."""
        self.assertEqual(media.list_media(self.entry_id)["data"], [])
        
        media.add_media(self.entry_id, str(self.source_media_file))
        list_result = media.list_media(self.entry_id)
        self.assertEqual(list_result["status"], "success")
        self.assertIn(self.source_media_file.name, list_result["data"])
        
        remove_result = media.remove_media(self.entry_id, self.source_media_file.name)
        self.assertEqual(remove_result["status"], "success")
        self.assertEqual(media.list_media(self.entry_id)["data"], [])
--- END OF FILE: offjournal/tests/test_media.py ---

--- START OF FILE: offjournal/tests/test_mood.py ---
# tests/test_mood.py

import unittest
import tempfile
import shutil
from pathlib import Path

import core.mood as mood

class TestMoodModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary directory for all mood analysis tests."""
        cls.test_dir = tempfile.mkdtemp(prefix="offjournal_mood_test_")
        mood.ENTRIES_DIR = Path(cls.test_dir)

        cls.positive_id = "20250715100000"
        (mood.ENTRIES_DIR / f"{cls.positive_id}_positive_day.md").write_text(
            "Estou muito feliz e animado hoje!", encoding="utf-8"
        )

        cls.negative_id = "20250715100100"
        (mood.ENTRIES_DIR / f"{cls.negative_id}_negative_day.md").write_text(
            "Me sinto triste e frustrado.", encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory after all tests."""
        shutil.rmtree(cls.test_dir)

    def test_analyze_positive_entry(self):
        """Test mood analysis on a predominantly positive entry."""
        result = mood.analyze_entry_mood(self.positive_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["mood"], "Positivo")
        self.assertGreater(result["positive_score"], result["negative_score"])

    def test_analyze_negative_entry(self):
        """Test mood analysis on a predominantly negative entry."""
        result = mood.analyze_entry_mood(self.negative_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["mood"], "Negativo")
        self.assertGreater(result["negative_score"], result["positive_score"])

    def test_analyze_non_existent_entry(self):
        """Test analyzing an entry that does not exist."""
        result = mood.analyze_entry_mood("nonexistent123")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("não encontrada", result["message"])
--- END OF FILE: offjournal/tests/test_mood.py ---

--- START OF FILE: offjournal/tests/test_planner.py ---
# tests/test_planner.py

import unittest
import tempfile
from pathlib import Path

import core.planner as planner

class TestPlannerModule(unittest.TestCase):
    def setUp(self):
        """Create a temporary file for the planner JSON for each test."""
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        planner.PLANNER_FILE = Path(self.temp_dir_obj.name) / "planner.json"

    def tearDown(self):
        """Clean up the temporary directory and file."""
        self.temp_dir_obj.cleanup()

    def test_get_events_empty(self):
        """Test getting events when the planner file doesn't exist."""
        self.assertEqual(planner.get_events(), [])

    def test_add_event_success(self):
        """Test successfully adding a new event."""
        result = planner.add_event("2025-12-25", "Natal")
        self.assertEqual(result["status"], "success")
        
        events = planner.get_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Natal")

    def test_add_event_invalid_date(self):
        """Test adding an event with an invalid date format."""
        result = planner.add_event("25-12-2025", "Data Inválida")
        self.assertEqual(result["status"], "error")

    def test_delete_event(self):
        """Test successfully deleting an event."""
        add_result = planner.add_event("2025-07-15", "Para Deletar")
        event_id = add_result["data"]["id"]
        
        delete_result = planner.delete_event(event_id)
        self.assertEqual(delete_result["status"], "success")
        
        self.assertEqual(len(planner.get_events()), 0)
        
    def test_delete_non_existent_event(self):
        """Test deleting an event ID that does not exist."""
        result = planner.delete_event(999)
        self.assertEqual(result["status"], "error")
--- END OF FILE: offjournal/tests/test_planner.py ---

--- START OF FILE: offjournal/tests/test_utils.py ---
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

    def test_read_and_write_file(self):
        """Test the cycle of writing to and reading from a file."""
        test_file = self.temp_dir / "testfile.txt"
        content = "Hello, off.journal!"
        utils.write_file(str(test_file), content)
        read_content = utils.read_file(str(test_file))
        self.assertEqual(content, read_content)

    def test_read_file_not_found(self):
        """Test that read_file raises FileNotFoundError for a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            utils.read_file(str(self.temp_dir / "nonexistent_file.txt"))

    def test_get_current_timestamp_format(self):
        """Test the format of the generated timestamp."""
        ts_default = utils.get_current_timestamp()
        self.assertRegex(ts_default, r"\d{14}")

    def test_validate_non_empty_string(self):
        """Test the string validation utility."""
        self.assertTrue(utils.validate_non_empty_string("valid"))
        self.assertFalse(utils.validate_non_empty_string(""))
        self.assertFalse(utils.validate_non_empty_string("   "))
--- END OF FILE: offjournal/tests/test_utils.py ---

```
