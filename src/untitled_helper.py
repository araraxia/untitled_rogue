#!/usr/bin/env python3
# Untitled Helper Module
# Aria Corona Feb 17th, 2025

import tkinter as tk
from tkinter import font
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

    
    def destroy_all_widgets(self, root):
        for widget in root.winfo_children():
            logger.debug(f"Destroying widget: {widget}")
            widget.destroy()
            
    
    def destroy_listed_widgets(self, widgets):
        for widget in widgets:
            logger.debug(f"Destroying widget: {widget}")
            widget.destroy() 
    
    
    def measure_font_size(self, font_settings):
        logger.debug("Measuring font size.")
        
        test_font = font.Font(family=font_settings[0], size=font_settings[1], weight=font_settings[2])
        width = test_font.measure("W")  # Measure the width of a character
        height = test_font.metrics("linespace")  # Measure the height of a character
        logger.debug(f"Character size in pixels: {width}x{height}")
        
        body_height = (self.window_height - (height * 2) - (self.frame_pad * 3) - (self.border_thickness * 3))
        body_width = (self.window_width - self.frame_pad - self.border_thickness)
        
        tile_x = body_width // width
        tile_y = body_height // height
        
        logger.debug(f"Tile size in characters: {tile_x}x{tile_y}")
        logger.debug(f"Body frame height: {body_height}")
        logger.debug(f"Body frame width: {body_width}")
        
        return tile_x, tile_y, width, height, body_width, body_height