import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext, messagebox, simpledialog, Toplevel
import json, os, keyboard, threading
#import config
from datetime import datetime

PLAYLIST_FILE = "Musicplayer/data/playlist.json"
CONFIG_FILE = "Musicplayer/config/config.json"

class GUI:
    def __init__(self, command_handler, title="Command Window"):
        self.command_handler = command_handler
        #self.music_instance = music_instance

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("450x270")

        self.is_shown = True
        self.hide_warning = True
        self.menu()
        self.log_tutorail()

    def menu(self):
        #Eingabe Feld für Befehle
        self.entry = ttk.Entry(self.root, width=35)
        self.entry.pack(pady=10, padx=120, side=tk.TOP, fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)

        #Log Bereich
        self.log_section = LogSection(self.root)

        #Exit
        ttk.Button(self.root,
                  text="Exit",
                  command=self.exit_program).pack(side="left",
                                               pady=10, padx=5,
                                               anchor=tk.NW,
                                               fill=tk.X, expand=True)

        #Hide
        ttk.Button(self.root,
                  text="Hide",
                  command=self.show_window).pack(side="left",
                                                 pady=10, padx=5,
                                                 anchor=tk.NW,
                                                 fill=tk.X, expand=True)
        
        #Resize
        ttk.Button(self.root,
                  text="Resize",
                  command=self.open_resize_window).pack(side="left",
                                                        pady=10, padx=5,
                                                        anchor=tk.NW,
                                                        fill=tk.X, expand=True)
        
        #Settings
        ttk.Button(self.root,
                  text="Settings",
                  command=self.open_settings_window).pack(side="left",
                                                        pady=10, padx=5,
                                                        anchor=tk.NW,
                                                        fill=tk.X, expand=True)

        self.root.after(100, self.Hotkey)

    #Erstellt einen neuen Thread für den eingegebenen Befehl
    def on_enter(self, event=None):
        cmd = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        threading.Thread(target=self.command_handler, args=(cmd,), daemon=True).start()

        if cmd.lower() in ["quit", "exit", "beenden", "stop"]:
            self.root.quit()

    def run(self):
        self.root.mainloop()

    def exit_program(self):
        self.command_handler("stop")
        self.root.quit()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    #Versteckt das Fenster oder lässt es wieder erscheinen (Fenster ist während es versteckt ist NICHT im Task-Manager sichtbar)
    def show_window(self):
        if self.is_shown:
            self.root.withdraw()
            self.is_shown = False
            self.show_hide_warning()
        else:
            self.root.deiconify()
            self.is_shown=True

    def show_hide_warning(self):
        config = self.load_config()
        show_popup = config.get("SHOW_HIDE_POPUP", True)

        if show_popup and self.hide_warning:
            hotkey = config.get("HOTKEYS", {}).get("hide", "f11")
            messagebox.showinfo("Info", f"Das Fenster wurde versteckt.\nDrücken Sie '{hotkey}' um es wieder anzuzeigen.\nPop-Up kann in den Settings geändert werden.")

            config["SHOW_HIDE_POPUP"] = False
            self.hide_warning = False
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

    def Hotkey(self):
        if hasattr(self, "current_hotkey"):
            try:
                keyboard.remove_hotkey(self.current_hotkey)
            except Exception:
                pass

        self.config = self.load_config()
        hotkey = self.config.get("HOTKEYS", {}).get("hide", "f11")
        keyboard.add_hotkey(hotkey, self.show_window, suppress=True)

        self.current_hotkey = hotkey
        self.root.after(75, self.Hotkey)

    def log_tutorail(self):
        tutorial_messages = [
            "Welcome.",
            "To add a playlist, go to Settings and click on 'Add Playlist'.",
            "To play a playlist, type the tag in the searchbar and press Enter.",
            "You can add 'shuffle' at the end of your command to play the playlist in shuffle mode.",
            "Enter 'help' in the searchbar to see all available commands."
        ]

        for message in tutorial_messages:
            self.log_message(message + "\n", level='INFO')

    #Button Funktionen
    def log_message(self, message, level='INFO'):
        self.log_section.logging(message, level)

    def open_settings_window(self):
        SettingsWindow(self.root, self)
    
    def open_resize_window(self):
        Resize_Window(self.root, self)

class LogSection():
    def __init__(self, master: tk.Widget):
        self.log = scrolledtext.ScrolledText(master,
                                             height=10, width=15,
                                             state='disabled',
                                             wrap='word',
                                             bg='black', fg='white')
        self.log.pack(side='bottom',
                      pady=5, padx=5,
                      anchor="n",
                      fill=tk.X, expand=True)
        self.log_tags()
        
    def log_tags(self):
        self.log.tag_config('INFO', foreground='white')
        self.log.tag_config('ERROR', foreground='red')
        self.log.tag_config('TIME', foreground='gray')
        self.log.tag_config('DEBUG', foreground='blue')
        self.log.tag_config('SUCCESS', foreground='green')

    def logging(self, message: str, level: str = 'INFO'):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log.config(state='normal')
        self.log.insert('end', f"{timestamp} ", 'TIME')
        self.log.insert('end', f"{message}\n", level)
        self.log.config(state='disabled')
        self.log.yview('end')

class SettingsWindow(tk.Toplevel):
    def __init__(self, master, gui_ref):
        super().__init__(master)
        self.title("Settings")
        self.geometry("300x250")
        self.gui = gui_ref

        self.show_popup_var = tk.BooleanVar(value=self.gui.load_config().get("SHOW_HIDE_POPUP", True))
        ttk.Checkbutton(self, text="Show Hide Popup",
                        variable=self.show_popup_var,
                        command=self.toggle_hide_popup).pack(pady=5,
                                                             padx=5,
                                                             anchor="nw")
        
        ttk.Label(self, text="Add Playlist", font=("Arial", 12)).pack(pady=10,
                                                                 padx=5,
                                                                 anchor="nw")
        
        ttk.Button(self, text="Add Playlist", command=self.open_add_playlist_window).pack(pady=4,
                                                                                          padx=5,
                                                                                          anchor="nw")
        
        ttk.Label(self, text="Change Hide Hotkey", font=("Arial", 12)).pack(pady=10,
                                                                        padx=5,
                                                                        anchor="nw")
        
        ttk.Button(self, text="Hotkeys", command=self.open_change_hotkeys_window).pack(pady=4,
                                                                                       padx=5,
                                                                                       anchor="nw")
        
    def toggle_hide_popup(self):
        config = self.gui.load_config()
        config["SHOW_HIDE_POPUP"] = self.show_popup_var.get()

        self.gui.hide_warning = self.show_popup_var.get()

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        self.gui.log_message("Hide Popup setting updated\n", level='SUCCESS')

    def open_add_playlist_window(self):
        Setting_Playlist(self, self.gui).adding_playlist()

    def open_change_hotkeys_window(self):
        Setting_Hotkeys(self, self.gui).changing_hotkeys()
        
class Setting_Playlist(tk.Toplevel):
    def __init__(self, master, gui_ref):
        super().__init__(master)
        self.title("Add Playlist")
        self.geometry("350x250")
        self.gui = gui_ref

    def adding_playlist(self):
        ttk.Label(self, text="Add Playlist", font=("Arial", 14)).pack(pady=8,
                                                                      padx=5,
                                                                      anchor="n")

        #Tag
        ttk.Label(self,text="Music Tag", font=("Arial", 12)).pack(pady=8,
                                                                  padx=15,
                                                                  anchor="nw")

        self.tag_entry = ttk.Entry(self, width=25)
        self.tag_entry.pack(pady=4,
                            padx=10,
                            anchor="nw")
        
        #Link
        ttk.Label(self, text="Music Link", font=("Arial", 12)).pack(pady=8,
                                                                    padx=15,
                                                                    anchor="nw")
        
        self.link_entry = ttk.Entry(self, width=40)
        self.link_entry.pack(pady=4,
                             padx=10,
                             anchor="nw")
        
        #Buttons
        ttk.Button(self, text="Safe", command=self.save_added).pack(pady=10,padx=5,
                                                                    side="right",
                                                                    anchor="n")
        
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=10,
                                                                  padx=5,
                                                                  side="left",
                                                                  anchor="n")

    def save_added(self):
        new_tag = self.tag_entry.get().strip()
        new_playlist = self.link_entry.get().strip()

        if not new_tag and not new_playlist:
            self.gui.log_message("Ungültige Eingabe\n", level='ERROR')
            return
                
        try:
            with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
                    playlist_config = json.load(f)
        except FileNotFoundError:
                playlist_config = {"PLAYLIST": {}}

        if new_tag in playlist_config.get("PLAYLIST", {}):
            self.gui.log_message("Tag bereits vorhanden\n", level='ERROR')
            if messagebox.askyesno("Playlist ersetzen?", "Der Tag ist bereits vorhanden. Möchten Sie die Playlist ersetzen?"):
                self.override_playlist(playlist_config, new_tag, new_playlist)
                self.gui.log_message("Link überschrieben\n", level='SUCCESS')
            else:
                self.gui.log_message("Playlist nicht überschrieben\n", level='INFO')

            return

        if "PLAYLIST" not in playlist_config:
            playlist_config["PLAYLIST"] = {}

        playlist_config["PLAYLIST"][new_tag] = new_playlist

        with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(playlist_config, f, ensure_ascii=False, indent=4)

            self.gui.log_message("Tag und Link gespeichert\n", level='SUCCESS')

        self.tag_entry.delete(0, 'end')
        self.link_entry.delete(0, 'end')

        self.tag_entry.focus()

    def override_playlist(self, playlist_config, new_tag, new_playlist):
        playlist_config["PLAYLIST"][new_tag] = new_playlist
        with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(playlist_config, f, ensure_ascii=False, indent=4)

class Setting_Hotkeys(tk.Toplevel):
    def __init__(self, master, gui_ref):
        super().__init__(master)
        self.title("Change Hotkeys")
        self.geometry("300x100")
        self.gui = gui_ref
    
    def changing_hotkeys(self):
        ttk.Label(self, text="Press Button to change Hotkey", font=("Arial", 12)).pack(pady=5,
                                                                                       padx=5,
                                                                                       anchor="n")

        ttk.Button(self, text="Change Hide Hotkey", command=self.save_hotkeys).pack(pady=5,
                                                                                    padx=5,
                                                                                    anchor="n")

    def save_hotkeys(self):
        hotkey = keyboard.read_hotkey(suppress=True)
        hotkey = self.convert_modifiers(hotkey)
        self.gui.log_message(f"Hotkey detectet: {hotkey}\n", level='DEBUG')

        self.config = self.gui.load_config()

        if "HOTKEYS" not in self.config:
            self.config["HOTKEYS"] = {}
        self.config["HOTKEYS"]["hide"] = hotkey

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

        self.gui.log_message("New Hotkey saved\n", level='SUCCESS')

        self.destroy()

    def convert_modifiers(self, hotkey: str) -> str:
        modifiers = {
            "strg": "ctrl",
            "umschalt": "shift",
            "alt": "alt",
            "win": "windows",
            "cmd": "windows"
        }

        parts = hotkey.lower().split('+')
        parts = [modifiers.get(part, part) for part in parts]
        return '+'.join(parts)

class Resize_Window(tk.Toplevel):
    def __init__(self, master, gui_ref):
        super().__init__(master)
        self.title("Resize Window")
        self.geometry("250x250")
        self.gui = gui_ref

        ttk.Label(self, text="Enter new Size", font=("Arial", 14)).pack(pady=8,
                                                                        padx=5,
                                                                        anchor="n")

        #Width
        ttk.Label(self,text="Width", font=("Arial", 12)).pack(pady=8,
                                                              padx=15,
                                                              anchor="nw")
        
        self.width_entry = ttk.Entry(self, width=25)
        self.width_entry.pack(pady=4,
                              padx=10,
                              anchor="nw")
        
        #Height
        ttk.Label(self, text="Height", font=("Arial", 12)).pack(pady=8,
                                                                padx=15,
                                                                anchor="nw")
        
        self.height_entry = ttk.Entry(self, width=25)
        self.height_entry.pack(pady=4,
                               padx=10,
                               anchor="nw")
        
        ttk.Button(self, text="Safe", command=self.save_resize).pack(pady=10,padx=5,
                                                                     side="right",
                                                                     anchor="n")
        
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=10,padx=5,
                                                                  side="left",
                                                                  anchor="n")
        
        ttk.Button(self, text="Reset", command=self.reset_resize).pack(pady=10,padx=5,
                                                                       side="bottom",
                                                                       anchor="n")
        
    def save_resize(self):
        new_width = self.width_entry.get().strip()
        new_height = self.height_entry.get().strip()

        if not new_width.isdigit() or not new_height.isdigit():
            self.gui.log_message("Ungültige Eingabe\n", level='ERROR')
            return

        self.gui.root.geometry(f"{new_width}x{new_height}")
        self.gui.log_message("Fenstergröße geändert\n", level='SUCCESS')

        self.width_entry.delete(0, 'end')
        self.height_entry.delete(0, 'end')

        #self.destroy()

    def reset_resize(self):
        self.gui.root.geometry("450x300")
        self.gui.log_message("Fenstergröße auf Standard zurückgesetzt\n", level='INFO')
        self.width_entry.delete(0, 'end')
        self.height_entry.delete(0, 'end')



if __name__ == "__main__":
    def dummy_command_handler(cmd):
        gui.log_message(f"{cmd}\n", level='INFO')

    gui = GUI(command_handler=dummy_command_handler, title="Test Command Window")
    gui.run()

