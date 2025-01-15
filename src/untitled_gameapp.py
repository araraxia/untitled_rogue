#!/usr/bin/env python3

import sys, os
import tkinter as tk
from tkinter import messagebox, font

loggerdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'loggers')
sys.path.append(loggerdir)        

from untitled_logger import logger # type: ignore

class Untgap:
    def __init__(self,
            root,
            width=1200,
            height=800,
            bg='black',
            font="Courier",
            font_size=14,
            font_weight="normal"
            ):
        
        logger.debug("Initializing untitled game application.")
        self.root = root
        self.bg=bg
        self.width=width
        self.height=height
        self.font = (font, font_size, font_weight)
        self.current_screen = "main_menu"
        
        logger.debug("Initializing root window.")
        self.root.title("Untitled Rogue")
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg=bg)
        self.root.bind('<KeyPress>', self.on_key_press)
        
        logger.debug("Measuring font size.")
        self.tile_x, self.tile_y, self.origin = self.measure_font_size(self.font)
        
    def on_key_press(self, event):
        if self.current_screen == "main_menu":
            self.main_menu_key_press(event)

    def main_menu_key_press(self, event):
        if event.keysym == 'Escape':
            self.root.quit()
            pass
        
    def measure_font_size(self, font_settings):
        test_font = font.Font(family=font_settings[0], size=font_settings[1], weight=font_settings[2])
        width = test_font.measure("W")  # Measure the width of a character
        height = test_font.metrics("linespace")  # Measure the height of a character
        logger.debug(f"Character size in pixels: {width}x{height}")
        
        tile_x = self.width // width
        tile_y = self.height // height
        
        origin_point = (int((self.width % width) / 2), int((self.height % height) / 2))
        
        logger.debug(f"Tile size in characters: {tile_x}x{tile_y}")
        logger.debug(f"Origin point: {origin_point}")
        
        return tile_x, tile_y, origin_point

    def 