import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext, messagebox, simpledialog, Toplevel
import json, os, keyboard, threading
#import config
from datetime import datetime

CONFIG_FILE = "Musicplayer/data/playlist.json"

class GUI:
    def __init__(self, command_handler, title="Command Window"):
        self.command_handler = command_handler

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("450x300")

        self.is_shown = True

        #Eingabe Feld für Befehle
        self.entry = ttk.Entry(self.root, width=35)
        self.entry.pack(pady=10, padx=120, side=tk.TOP, fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)

        #Log Bereich
        self.log_section = LogSection(self.root)

        #Exit
        ttk.Button(self.root,
                  text="Exit",
                  command=self.root.quit).pack(side="left",
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

    #Versteckt das Fenster oder lässt es wieder erscheinen (Fenster ist während es versteckt ist NICHT im Task-Manager sichtbar)
    def show_window(self):
        if self.is_shown:
            self.root.withdraw()
            self.is_shown = False
        else:
            self.root.deiconify()
            self.is_shown=True

    def Hotkey(self):
        if keyboard.is_pressed('F11'):  #3
            self.show_window()

        self.root.after(75, self.Hotkey)


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
                      anchor="center",
                      fill=tk.X, expand=True)
        self.log_tags()
        
    def log_tags(self):
        self.log.tag_config('INFO', foreground='white')
        self.log.tag_config('WARN', foreground='orange')
        self.log.tag_config('ERROR', foreground='red')
        self.log.tag_config('TIME', foreground='gray')

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
        self.geometry("300x370")
        self.gui = gui_ref

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
            self.gui.log_message("Error: Kein Inhalt", level='ERROR')
            return
                
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    playlist_config = json.load(f)
        except FileNotFoundError:
                playlist_config = {"PLAYLIST": {}, "HOTKEYS": {}}

        if new_tag in playlist_config.get("PLAYLIST", {}):
            self.gui.log_message("Error: Tag bereits vorhanden", level='ERROR')
            return

        if "PLAYLIST" not in playlist_config:
            playlist_config["PLAYLIST"] = {}

        playlist_config["PLAYLIST"][new_tag] = new_playlist

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(playlist_config, f, ensure_ascii=False, indent=4)

            self.gui.log_message("Tag und Link gespeichert", level='INFO')

        self.tag_entry.delete(0, 'end')
        self.link_entry.delete(0, 'end')

        self.tag_entry.focus()

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
            self.gui.log_message("Error: Ungültige Eingabe", level='ERROR')
            return

        self.gui.root.geometry(f"{new_width}x{new_height}")
        self.gui.log_message("Fenstergröße geändert", level='INFO')

        self.width_entry.delete(0, 'end')
        self.height_entry.delete(0, 'end')

        #self.destroy()

    def reset_resize(self):
        self.gui.root.geometry("450x300")
        self.gui.log_message("Fenstergröße auf Standard zurückgesetzt", level='INFO')
        self.width_entry.delete(0, 'end')
        self.height_entry.delete(0, 'end')



if __name__ == "__main__":
    def dummy_command_handler(cmd):
        gui.log_message(f"{cmd}", level='INFO')

    gui = GUI(command_handler=dummy_command_handler, title="Test Command Window")
    gui.run()

