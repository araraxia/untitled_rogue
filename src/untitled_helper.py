#!/usr/bin/env python3
# Untitled Helper Module
# Aria Corona Feb 17th, 2025

import tkinter as tk
from loggers.untitled_logger import logger
import os

CONF_PATH = os.path.join('conf', 'conf.json')
class untitledHelper:
    def __init__(self, conf=CONF_PATH):
        logger.debug("Initializing untitled helper module.")
        self.conf = conf
        
        
    def create_frame(self, parent, bg, borderwidth, relief, **kwargs):
        border_frame = tk.Frame(
            parent,
            bg=bg,
            borderwidth=borderwidth,
            relief=relief,
            **kwargs
        )
        
        inner_frame = tk.Frame(
            border_frame,
            bg=bg,
            **kwargs
        )
        
        frame = {
            'inner': inner_frame,
            'border': border_frame
        }
        
        return frame