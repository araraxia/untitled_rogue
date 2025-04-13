import logging
import tkinter as tk
from untitled_gameapp import Untgap

logger = logging.getLogger(__name__)


class UntitleScreen(Untgap):
    def __init__(self):
        Untgap.root
        self.conf = Untgap.conf
        self.loaded_components = []
        self.init_title_screen()

    def load_title(self, x_pos, y_pos):
        self.title_label.place(x=x_pos, y=y_pos, anchor="center")
        self.loaded_components.append({"title_label": self.title_label})

    def init_title_screen(self):
        logger.debug("Creating title screen.")
        title_message = "untitled rogue\n\npress any key to start"
        self.title_label = tk.Label(
            Untgap.root, text=title_message, font=self.font, bg=self.bg, fg=self.fg
        )
    
    
    
    def go_to_main_menu(self, event):
        logger.debug("Key pressed. Transitioning to main menu.")
        Untgap.root.unbind("<KeyPress>")
        Untgap.current_screen = "main_menu"
        Untgap.init_components()
    
    def run(self):
        logger.debug("Running title screen.")
        self.title_label.place(x=Untgap.window_width // 2,
                               y=Untgap.window_height // 2,
                               anchor="center")
        self.loaded_components.append({"title_label": self.title_label})
        
        # Bind key press event to start the game
        Untgap.root.bind("<KeyPress>", self.go_to_main_menu)