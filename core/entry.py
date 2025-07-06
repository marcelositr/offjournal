import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/entries")

def create_entry():
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(DATA_DIR, f"{date_str}.md")
    if os.path.exists(filename):
        print(f"Entrada para {date_str} já existe.")
    else:
        with open(filename, "w") as f:
            f.write(f"# Entrada do diário - {date_str}\n\n")
        print(f"Nova entrada criada: {filename}")
    # Abre o arquivo no editor padrão do sistema (nano como fallback)
    editor = os.getenv("EDITOR", "nano")
    os.system(f"{editor} {filename}")

def list_entries():
    if not os.path.exists(DATA_DIR):
        print("Nenhuma entrada encontrada.")
        return
    files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".md"))
    if not files:
        print("Nenhuma entrada encontrada.")
    else:
        print("Entradas encontradas:")
        for f in files:
            print(f" - {f}")
