#!/usr/bin/env python3

import sys, os, json
import tkinter as tk
from tkinter import font

loggerdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'loggers')
sys.path.append(loggerdir)        

from untitled_logger import logger # type: ignore

class Untgap:
    def __init__(self, root, conf_path='conf/conf.json'):
        
        logger.debug(f"Initializing Untitled Game Application with configuration file {conf_path}.")
        conf = self.load_conf(conf_path)
        
        self.display = conf['display']
        self.window_tyle = self.display['type']
        self.window_width = self.display['width']
        self.window_height = self.display['height']
        self.font_family = self.display['fontFamily']
        self.font_size = self.display['fontSize']
        self.font_weight = self.display['fontWeight']
        self.font = (self.font_family, self.font_size, self.font_weight)
        self.frame_pad = self.display['framePadding']
        self.highlight_thickness = self.display['highlightThickness']
        
        self.colors = conf['colors']
        self.bg = self.colors['background']
        self.fg = self.colors['foreground']
        self.border = self.colors['border']
        self.border_bg = self.colors['border2']
        
        self.keybinds = conf['keybinds']
        
        
        logger.debug("Initializing untitled game application.")
        self.root = root
        self.current_screen = "title_screen"
        
        logger.debug("Initializing root window.")
        self.root.title("Untitled Rogue")
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.bg)
        self.root.bind('<KeyPress>', self.on_key_press)
        
        logger.debug("Measuring font size.")
        self.tile_x, self.tile_y, self.font_width, self.font_height = self.measure_font_size(self.font)

        logger.debug("Initializing frames.")
        self.header_frame, self.body_frame, self.footer_frame = self.init_frames(self.frame_pad)
        
        if self.current_screen == "title_screen":
            logger.debug("Creating title screen.")
            #self.create_title_screen()
    
    
    def load_conf(self, path):
        logger.debug("Loading configuration from %s", path)
        
        with open(path, 'r') as config_file:
            config = json.load(config_file)
        
        logger.debug("Configuration loaded successfully.")
        return config
    
    
    def create_frame(self, **kwargs):
        return tk.Frame(
            self.root,
            bg=self.bg,
            highlightbackground=self.border_bg,
            highlightcolor=self.border,
            highlightthickness=self.highlight_thickness,
            **kwargs
        )
    
    
    def init_frames(self, frame_pad):
        logger.debug("Initializing frames.")
        
        header_frame = self.create_frame(height=self.font_height)
        header_frame.pack(side="top", fill="x", padx=frame_pad, pady=frame_pad)

        body_frame = self.create_frame()
        body_frame.pack(side="top", fill="both", expand=True, padx=frame_pad, pady=frame_pad)

        footer_frame = self.create_frame(height=self.font_height)
        footer_frame.pack(side="bottom", fill="x", padx=frame_pad, pady=frame_pad)
        
        return header_frame, body_frame, footer_frame

        
        
    def create_title_screen(self, font):
        logger.debug("Creating title screen.")
        title_message = "untitled rogue"
        


    def measure_font_size(self, font_settings):
        test_font = font.Font(family=font_settings[0], size=font_settings[1], weight=font_settings[2])
        width = test_font.measure("W")  # Measure the width of a character
        height = test_font.metrics("linespace")  # Measure the height of a character
        logger.debug(f"Character size in pixels: {width}x{height}")
        
        tile_x = self.window_width // width
        tile_y = self.window_height // height
        
        origin_point = (int((self.window_width % width) / 2), int((self.window_height % height) / 2))
        
        logger.debug(f"Tile size in characters: {tile_x}x{tile_y}")
        logger.debug(f"Origin point: {origin_point}")
        
        return tile_x, tile_y, width, height


    # Event handlers

    def on_key_press(self, event):
        if self.current_screen == "title_screen":
            self.title_screen_key_press(event)
        
        if self.current_screen == "main_menu":
            self.main_menu_key_press(event)


    def main_menu_key_press(self, event):
        if event.keysym == 'Escape':
            self.root.quit()
            pass
        
        
    def title_screen_key_press(self, event):
        if event.keysym == 'Escape':
            self.current_screen == "main_menu"
            pass