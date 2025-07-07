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

    # TODO: Re-implement other commands (export, crypto) in a similar fashion.

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
        # Fallback for other data-carrying responses
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
        # Use sys.executable to ensure the same Python interpreter is used
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
