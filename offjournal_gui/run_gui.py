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
