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
        
        self.display_conf = conf['display']
        self.window_tyle = self.display_conf['type']
        self.window_width = self.display_conf['width']
        self.window_height = self.display_conf['height']
        self.font_family = self.display_conf['fontFamily']
        self.font_size = self.display_conf['fontSize']
        self.font_weight = self.display_conf['fontWeight']
        self.font = (self.font_family, self.font_size, self.font_weight)
        self.frame_pad = self.display_conf['framePadding']
        self.border_thickness = self.display_conf['highlightThickness']
        self.frame_relief = self.display_conf['frameRelief']
        self.resizable = self.display_conf['resizable']
        
        self.color_conf = conf['colors']
        self.bg = self.color_conf['background']
        self.fg = self.color_conf['foreground']
        self.frame_color = self.color_conf['frame']
        self.border_bg = self.color_conf['border2']
        
        self.header_conf = conf['header']
        self.footer_conf = conf['footer']
        
        self.keybind_conf = conf['keybinds']
        
        logger.debug("Initializing untitled game application.")
        self.root = root
        self.current_screen = "title_screen"
        
        logger.debug("Initializing root window.")
        self.root.title("Untitled Rogue")
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(self.resizable, self.resizable)
        self.root.configure(bg=self.bg)
        self.root.bind('<KeyPress>', self.on_key_press)
        
        self.tile_x, self.tile_y, self.font_width, self.font_height, self.body_width, self.body_height = self.measure_font_size(self.font)

        self.header_frame, self.body_frame, self.footer_frame = self.init_frames(self.font_height, self.header_conf['pady'], self.footer_conf['pady'])
        
        if self.current_screen == "title_screen":
            logger.debug("Loading title screen.")
            self.title_label = self.init_title_screen()
            self.load_title(self.title_label)
            
        #self.pack_game_frames()

    
    def load_conf(self, path):
        logger.debug("Loading configuration from %s", path)
        
        with open(path, 'r') as config_file:
            config = json.load(config_file)
        
        logger.debug("Configuration loaded successfully.")
        return config
    
    
    def pack_game_frames(self):
        logger.debug("Packing game frames.")
        
        header_frame = self.header_frame[0]
        header_border = self.header_frame[1]
        body_frame = self.body_frame[0]
        body_border = self.body_frame[1]
        footer_frame = self.footer_frame[0]
        footer_border = self.footer_frame[1]
        
        header_border.pack(side="top", fill="x", padx=self.frame_pad, pady=self.frame_pad)
        header_frame.pack(side="top", fill="x")
        
        body_border.pack(side="top", fill="both", expand=True, padx=self.frame_pad, pady=self.frame_pad)
        body_frame.pack(side="top", fill="both", expand=True)
        
        footer_border.pack(side="bottom", fill="x", padx=self.frame_pad, pady=self.frame_pad)
        footer_frame.pack(side="bottom", fill="x")
    
    
    def create_frame(self, **kwargs):
        logger.debug("Creating frame objects.")
        border_frame = tk.Frame(
            self.root,
            bg=self.frame_color,
            borderwidth=self.border_thickness,
            relief=self.frame_relief,
            **kwargs
        )
        
        inner_frame = tk.Frame(
            border_frame,
            bg=self.bg,
            **kwargs
        )
        
        return inner_frame, border_frame
    
    
    def init_frames(self, font_height, head_pady, foot_pady):
        logger.debug("Initializing frames.")
        
        logger.debug(f"Initializing header frame.")
        header_frame = self.create_frame(height=(font_height + head_pady))

        logger.debug(f"Initializing body frame.")
        body_frame = self.create_frame()
        
        logger.debug(f"Initializing footer frame.")
        footer_frame = self.create_frame(height=(font_height + foot_pady))
        
        return header_frame, body_frame, footer_frame

    
    def load_title(self, title):
        title.grid(row=1, column=1, sticky="nsew")
        
    
    
    def init_title_screen(self): ##########Left off here
        logger.debug("Creating title screen.")
        title_message = "untitled rogue"
        title_text = tk.Text()
        title_label = tk.Label(self.root, text=title_message)
        
        return title_label

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
        
        #origin_point = (int((self.window_width % width) / 2), int((self.window_height % height) / 2))
        
        logger.debug(f"Tile size in characters: {tile_x}x{tile_y}")
        #logger.debug(f"Origin point: {origin_point}")
        logger.debug(f"Body frame height: {body_height}")
        logger.debug(f"Body frame width: {body_width}")
        
        return tile_x, tile_y, width, height, body_width, body_height


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