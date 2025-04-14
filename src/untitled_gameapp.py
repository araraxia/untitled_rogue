#!/usr/bin/env python3

import sys, os, json
import tkinter as tk
from tkinter import font
from loggers.untitled_logger import logger  # type: ignore
from untitled_helper import untitledHelper
from untitle_screen import UntitleScreen
from untitled_game import UntGame
from main_menu import MainMenu


class Untgap:
    def __init__(self, root, conf_path="conf/conf.json"):
        logger.debug(
            f"Initializing Untitled Game Application with configuration file {conf_path}."
        )
        self.conf = self.load_conf(conf_path)

        self.display_conf = self.conf["display"]
        self.window_tyle = self.display_conf["type"]
        self.window_width = self.display_conf["width"]
        self.window_height = self.display_conf["height"]
        self.font_family = self.display_conf["fontFamily"]
        self.font_size = self.display_conf["fontSize"]
        self.font_weight = self.display_conf["fontWeight"]
        self.font = (self.font_family, self.font_size, self.font_weight)
        self.frame_pad = self.display_conf["framePadding"]
        self.border_thickness = self.display_conf["highlightThickness"]
        self.frame_relief = self.display_conf["frameRelief"]
        self.resizable = self.display_conf["resizable"]

        self.color_conf = self.conf["colors"]
        self.bg = self.color_conf["background"]
        self.fg = self.color_conf["foreground"]
        self.frame_color = self.color_conf["frame"]
        self.border_bg = self.color_conf["border2"]

        self.header_conf = self.conf["header"]
        self.footer_conf = self.conf["footer"]

        self.keybind_conf = self.conf["keybinds"]

        logger.debug("Initializing untitled game application.")
        self.root = root
        self.current_screen = "title_screen"

        logger.debug("Initializing root window.")
        self.root.title("Untitled Rogue")
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(self.resizable, self.resizable)
        self.root.configure(bg=self.bg)
        (
            self.font_width,
            self.font_height,
        ) = untitledHelper.measure_font_size(self.font)

        self.init_components()
        self.loaded_components = []

    def load_conf(self, path):
        logger.debug("Loading configuration from %s", path)

        with open(path, "r") as config_file:
            config = json.load(config_file)

        if config:
            logger.info("Configuration loaded successfully.")
            return config
        else:
            logger.error("Failed to load configuration.")
            sys.exit(1)

    ### Gen Methods ###
    def destroy_all_widgets(self):
        for widget in self.root.winfo_children():
            logger.debug(f"Destroying widget: {widget}")
            widget.destroy()
        return []

    def refresh_window(self):
        logger.debug("Refreshing window.")
        last_frame = []
        for widget in self.root.winfo_children():
            last_frame.append(widget)
        self.init_components()

    ### Init Method ###
    def init_components(self):
        (
            self.font_width,
            self.font_height,
        ) = untitledHelper.measure_font_size(self.font)
        logger.debug(f"init_components - current_screen: {self.current_screen}")

        if self.current_screen == "title_screen":
            self.destroy_all_widgets()
            logger.debug("Loading title screen.")
            untitle_screen = UntitleScreen()
            untitle_screen.run()

        elif self.current_screen == "main_menu":
            self.destroy_all_widgets()
            logger.debug("Loading main menu.")
            main_menu = MainMenu()
            main_menu.run()

        elif self.current_screen == "in_game":
            self.destroy_all_widgets()
            logger.debug("Loading game screen.")
            untitled_game = UntGame()
            untitled_game.run()
    
    
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
        if event.keysym == self.keybind_conf["pause"]:

            pass
