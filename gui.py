import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
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

        self.entry = tk.Entry(self.root, width=35)
        self.entry.grid(pady=10, padx=120, columnspan=2, sticky='w')
        self.entry.bind("<Return>", self.on_enter)

        self.is_shown = True
        self.is_resized = False

        tk.Button(self.root,
                  text="Exit",
                  command=self.root.quit).grid(row=1,
                                               column=0,
                                               pady=10, padx=115,
                                               sticky='w')

        tk.Button(self.root,
                  text="Hide",
                  command=self.show_window).grid(row=1,
                                                 column=0,
                                                 pady=10, padx=170,
                                                 sticky='w')
        
        tk.Button(self.root,
                  text="Resize",
                  command=self.resize).grid(row=1,
                                            column=0,
                                            pady=10, padx=230,
                                            sticky='w')
        
        tk.Button(self.root,
                  text="Settings",
                  command=self.resize).grid(row=1,
                                            column=0,
                                            pady=10, padx=300,
                                            sticky='w')

        self.root.after(100, self.Hotkey)


    def on_enter(self, event=None):
        cmd = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        threading.Thread(target=self.command_handler, args=(cmd,), daemon=True).start()

        if cmd.lower() in ["quit", "exit", "beenden", "stop"]:
            self.root.quit()

    def run(self):
        self.root.mainloop()

    def show_window(self):
        if self.is_shown:
            self.root.withdraw()
            self.is_shown = False
        else:
            self.root.deiconify()
            self.is_shown=True

    def Hotkey(self):
        if keyboard.is_pressed('F11'):
            self.show_window()

        self.root.after(75, self.Hotkey)

    def resize(self):
        if not self.is_resized:
            self.root.geometry("680x550")
            self.entry.config(width=60)
            self.is_resized = True
        else:
            self.root.geometry("450x300")
            self.entry.config(width=35)
            self.is_resized = False

if __name__ == "__main__":
    def dummy_command_handler(cmd):
        print(f"Command received: {cmd}")

    gui = GUI(command_handler=dummy_command_handler, title="Test Command Window")
    gui.run()