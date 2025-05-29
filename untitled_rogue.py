

import tkinter as tk
import json, pickle, sys
from functools import wraps
from src.loggers.untitled_logger import setup_logger
from src.untitled_title_screen import UntitledTitleScreen
from src.main_menu import MainMenu
from src.untitled_helper import untitledHelper

class UntitledRogueApp(tk.Tk):
    def __init__(self, config_path='conf/conf.json'):
        super().__init__()
        self.logger = setup_logger()
        self.title("Untitled Rogue")
        self.geometry("800x600")
        self.config = self.load_config(config_path)
        self.current_screen = "title"
        self.load_screen()


    def load_config(self, path):
        self.event_types = [
            "<Key>", "<KeyPress>", "<KeyRelease>", "<ButtonPress>", "<ButtonRelease>",
            "<Motion>", "<Enter>", "<Leave>", "<FocusIn>", "<FocusOut>",
            "<Configure>", "<Destroy>", "<Visibility>", "<Expose>",
            "<Map>", "<Unmap>", "<Activate>", "<Deactivate>",
        ]
        with open(path, 'r') as file:
            return json.load(file)
    
    def clear_root(func):
        def wrapper(self, *args, **kwargs):
            for widget in self.winfo_children():
                widget.destroy()
            self.logger.debug("Cleared root window.")
            return func(self, *args, **kwargs)
        return wrapper

    def load_screen(self):
        directory = {
            "title": self.load_title,
            "main_menu": self.load_main_menu,
        }
        if self.current_screen in directory:
            self.logger.debug(f"Loading screen: {self.current_screen}")
            directory[self.current_screen]()
        else:
            self.logger.error(f"Screen {self.current_screen} not found.")
            sys.exit(1)
        
    @untitledHelper.clear_root
    def load_title(self):
        title = UntitledTitleScreen(self,)
        title.load_title()
    
    @untitledHelper.clear_root
    def load_main_menu(self):
        main_menu = MainMenu(self,)
        
    def play_sound(self, sound):
        """
        Placeholder for sound playing functionality.
        This method should be implemented to play sounds.
        """
        self.logger.debug(f"Playing sound: {sound.name}")
        # Implement sound playing logic here
        pass
        
    
if __name__ == "__main__":
    app = UntitledRogueApp()
    app.mainloop()