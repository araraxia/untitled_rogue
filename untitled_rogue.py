

import tkinter as tk
import json, pickle
from src.loggers.untitled_logger import setup_logger
from src.untitled_title_screen import UntitledTitleScreen

class UntitledRogueApp(tk.Tk):
    def __init__(self, config_path='conf/conf.json'):
        super().__init__()
        self.logger = setup_logger()
        self.title("Untitled Rogue")
        self.geometry("800x600")
        
        self.config = self.load_config(config_path)
        
        self.load_title()

    def load_config(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def load_title(self):
        title = UntitledTitleScreen(self, self.config, self.logger)
        title.load_title()
    
if __name__ == "__main__":
    app = UntitledRogueApp()
    app.mainloop()