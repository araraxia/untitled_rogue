#!/usr/bin/env python3
# Aria Corona

from loggers.untitled_logger import logger
from untitled_helper import untitledHelper
import tkinter as tk

class UntitledTitleScreen:
    def __init__(self, root, conf):
        self.root = root
        self.conf = conf
    
    def load_title(self, title_label, x_pos, y_pos):
        title_label.place(x=x_pos, y=y_pos, anchor="center") 
        self.loaded_components.append({'title_label': title_label})
        

    def init_title_screen(self, font, bg, fg): 
        logger.debug("Creating title screen.")
        title_message = "untitled rogue\n\npress any key to start"
        title_label = tk.Label(self.root, text=title_message, font=font, bg=bg, fg=fg)

        return title_label