import sys
from core import entry

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <comando> [args]")
        return

    cmd = sys.argv[1]
    if cmd == "new":
        entry.create_entry()
    elif cmd == "list":
        entry.list_entries()
    else:
        print(f"Comando '{cmd}' não reconhecido.")

if __name__ == "__main__":
    main()
