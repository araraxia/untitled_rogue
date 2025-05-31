

import tkinter as tk
import json, pickle, sys, pygame
from functools import wraps
from src.loggers.untitled_logger import setup_logger
from src.untitled_title_screen import UntitledTitleScreen
from src.main_menu import MainMenu
from src.untitled_helper import untitledHelper

class UntitledRogueApp(tk.Tk):
    def __init__(self, config_path='conf/conf.json'):
        super().__init__()
        self.logger = setup_logger()
        self.audio_map = self.load_audio()
        self.config = self.load_config(config_path)
        self.current_screen = "title"
        self.title("Untitled Rogue")
        self.window_width = 800
        self.window_height = int((self.window_width * 3) // 4)
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(True, True)
        self.load_screen()

    # Init methods
    def load_audio(self):
        pygame.mixer.init()
        with open('conf/audio_mapping.json', 'r') as file:
            audio_map = json.load(file)
        return audio_map

    def load_config(self, path):
        self.event_types = [
            "<Key>", "<KeyPress>", "<KeyRelease>", "<ButtonPress>", "<ButtonRelease>",
            "<Motion>", "<Enter>", "<Leave>", "<FocusIn>", "<FocusOut>",
            "<Configure>", "<Destroy>", "<Visibility>", "<Expose>",
            "<Map>", "<Unmap>", "<Activate>", "<Deactivate>",
        ]
        with open(path, 'r') as file:
            return json.load(file)
    
    # Screen Loading Methods

    def load_screen(self):
        directory = {
            "title": self.load_title,
            "main_menu": self.load_main_menu,
            "char_creation": self.load_char_creation,
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
    
    @untitledHelper.clear_root
    def load_char_creation(self):
        from src.char_creation import CharCreator
        char_creator = CharCreator(self)
        char_creator.create_character()
        
    # Engine Methods
        
    def play_sound(self, sound_obj: object):
        """
        Placeholder for sound playing functionality.
        This method should be implemented to play sounds.
        """
        self.logger.debug(f"Playing sound: {sound_obj.name}")
        try:
            sound_obj.sound.play()
        except pygame.error as e:
            self.logger.error(f"Error playing sound {sound_obj.name}: {e}")
        except AttributeError:
            self.logger.error(f"Sound object {sound_obj.name} does not have a sound attribute.")
        pass
        
    
if __name__ == "__main__":
    app = UntitledRogueApp()
    app.mainloop()