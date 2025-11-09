import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import simpledialog
import threading
import keyboard
#import config
from datetime import datetime

class GUI:
    def __init__(self, command_handler, title="Command Window"):
        self.command_handler = command_handler

        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("450x300")

        self.is_shown = True
        self.is_resized = False

        #Log Fenster
        self.log = scrolledtext.ScrolledText(self.root,
                                             height=10, width=15,
                                             state='disabled',
                                             wrap='word',
                                             bg='black', fg='white')
        self.log.pack(side='bottom',
                      pady=5, padx=5,
                      anchor="center",
                      fill=tk.X, expand=True)

        #Eingabe Feld für Befehle
        self.entry = tk.Entry(self.root, width=35)
        self.entry.pack(pady=10, padx=120, side=tk.TOP, fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)

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
                  command=self.resize).pack(side="left",
                                            pady=10, padx=5,
                                            anchor=tk.NW,
                                            fill=tk.X, expand=True)
        
        #Settings
        ttk.Button(self.root,
                  text="Settings",
                  command=None).pack(side="left",
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

    #Ändert die aktuelle Fenstergröße zwischen zwei voreingestellten Größen
    def resize(self):
        if not self.is_resized:
            new_width = simpledialog.askinteger("Breite eingeben", "Neue Breite:")
            new_height = simpledialog.askinteger("Höhe eingeben", "Neue Höhe:")

            if new_width and new_height:
                self.root.geometry(f"{new_width}x{new_height}")
            self.is_resized = True
        else:
            self.root.geometry("450x300")
            self.is_resized = False

    def log_tags(self):
        self.log.tag_config('INFO', foreground='white')
        self.log.tag_config('WARN', foreground='orange')
        self.log.tag_config('ERROR', foreground='red')
        self.log.tag_config('TIME', foreground='gray')

    def log_message(self, message: str, level: str = 'INFO'):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log.config(state='normal')
        self.log.insert('end', f"{timestamp} ", 'TIME')
        self.log.insert('end', f"{message}\n", level)
        self.log.config(state='disabled')
        self.log.yview('end')

if __name__ == "__main__":
    def dummy_command_handler(cmd):
        gui.log_message(f"Erkannter Befehl: {cmd}", level='INFO')

    gui = GUI(command_handler=dummy_command_handler, title="Test Command Window")
    gui.run()

    '''
    Einstellungs Fenster einbauen
    -Hotkeys änderbar machen via Einstellungen  (3)
    -Playlist Link hinzufügen/ändern/entfernen  (4)
    -Playlist Tag bei Playlist hinzufügen  (5)
    -
    '''