#!/usr/bin/env python3

import sys, os, json
import tkinter as tk
from tkinter import font
from loggers.untitled_logger import logger # type: ignore
from main_menu import main_menu
class Untgap:
    def __init__(self, root, conf_path='conf/conf.json'):
        
        logger.debug(f"Initializing Untitled Game Application with configuration file {conf_path}.")
        self.conf = self.load_conf(conf_path)
        
        self.display_conf = self.conf['display']
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
        
        self.color_conf = self.conf['colors']
        self.bg = self.color_conf['background']
        self.fg = self.color_conf['foreground']
        self.frame_color = self.color_conf['frame']
        self.border_bg = self.color_conf['border2']
        
        self.header_conf = self.conf['header']
        self.footer_conf = self.conf['footer']
        
        self.keybind_conf = self.conf['keybinds']
        
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
        
        self.init_components()
        
        
    ### Gen Methods ###
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

    def destroy_all_widgets(self):
        for widget in self.root.winfo_children():
            logger.debug(f"Destroying widget: {widget}")
            widget.destroy()   
    
    def refresh_window(self):
        logger.debug("Refreshing window.")
        self.destroy_all_widgets()
        self.init_components()
    
    def load_conf(self, path):
        logger.debug("Loading configuration from %s", path)
        
        with open(path, 'r') as config_file:
            config = json.load(config_file)
        
        logger.debug("Configuration loaded successfully.")
        return config
    
    
    ### Init Method ###
    def init_components(self):
        self.tile_x, self.tile_y, self.font_width, self.font_height, self.body_width, self.body_height = self.measure_font_size(self.font)
        logger.debug(f"init_components - current_screen: {self.current_screen}")
        
        if self.current_screen == "title_screen":
            logger.debug("Loading title screen.")
            self.title_label = self.init_title_screen()
            self.load_title(self.title_label, self.window_width // 2, self.window_height // 2)
       
        elif self.current_screen == "in_game":
            game_frames = self.init_frames(self.font_height, self.header_conf['pady'], self.footer_conf['pady'])
            self.pack_game_frames(game_frames)
            
        elif self.current_screen == "main_menu":
            logger.debug("Loading main menu.")
            self.init_menu_screen()

      
    ### Game Frames ###
    def pack_game_frames(self, game_frames):
        logger.debug("Packing game frames.")
        
        header_frame = game_frames['header']['inner']
        header_border = game_frames['header']['border']
        body_frame = game_frames['body']['inner']
        body_border = game_frames['body']['border']
        footer_frame = game_frames['footer']['inner']
        footer_border = game_frames['footer']['border']
        
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
        
        frame = {
            'inner': inner_frame,
            'border': border_frame
        }
        
        return frame
    
    def init_frames(self, font_height, head_pady, foot_pady):
        logger.debug("Initializing frames.")
        
        logger.debug(f"Initializing header frame.")
        header_frame = self.create_frame(height=(font_height + head_pady))

        logger.debug(f"Initializing body frame.")
        body_frame = self.create_frame()
        
        logger.debug(f"Initializing footer frame.")
        footer_frame = self.create_frame(height=(font_height + foot_pady))
        
        game_frames = {
            'header': header_frame, 
            'body': body_frame, 
            'footer': footer_frame
        }
        
        return game_frames


    ### Title Screen ###
    def load_title(self, title_label, x_pos, y_pos):
        title_label.place(x=x_pos, y=y_pos, anchor="center") 
        
    def init_title_screen(self): 
        logger.debug("Creating title screen.")
        title_message = "untitled rogue\n\npress any key to start"
        title_label = tk.Label(self.root, text=title_message, font=self.font, bg=self.bg, fg=self.fg)

        return title_label


    ### Main Menu ###
    def init_menu_screen(self):
        self.main_menu = main_menu(self.root, self.conf)
        self.current_screen = self.main_menu.init_menu()
        

    ### Event handlers ###
    def on_key_press(self, event):
        if self.current_screen == "title_screen":
            logger.debug("Title screen key press.")
            self.title_screen_key_press(event)
        
        elif self.current_screen == "in_dungeon":
            logger.debug("In dungeon key press.")
            self.in_dungeon_key_press(event)
            
        elif self.current_screen == "main_menu":
            logger.debug("Main menu key press.")
            self.main_menu.handle_key_press(event)

    def wait_for_key_press(self):
        self.key_pressed = tk.StringVar()
        self.root.wait_variable(self.key_pressed)

    def in_dungeon_key_press(self, event):
        if event.keysym == self.keybind_conf['pause']:

            pass
        
    def title_screen_key_press(self, event):
        if event.keysym:
            logger.debug("Go to main_menu - Key pressed: %s", event.keysym)
            self.current_screen = "main_menu"
            logger.debug(f"title_screen_key_press - current_screen: {self.current_screen}")
            self.refresh_window()