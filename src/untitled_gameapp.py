#!/usr/bin/env python3

import sys, os, json
import tkinter as tk
from tkinter import font
from loggers.untitled_logger import logger  # type: ignore
from untitled_helper import untitledHelper
from untitled_title_screen import UntitledTitleScreen
from main_menu import main_menu


class Untgap:
    def __init__(self, root, conf_path="conf/conf.json"):
        logger.debug(
            f"Initializing Untitled Game Application with configuration file {conf_path}."
        )
        self.conf = self.load_conf(conf_path)

        self.display_conf = self.conf.get("display")
        self.window_tyle = self.display_conf.get("type")
        self.window_width = self.display_conf.get("width")
        self.window_height = self.display_conf.get("height")
        self.font_family = self.display_conf.get("fontFamily")
        self.font_size = self.display_conf.get("fontSize")
        self.font_weight = self.display_conf.get("fontWeight")
        self.font = (self.font_family, self.font_size, self.font_weight)
        self.frame_pad = self.display_conf.get("framePadding")
        self.border_thickness = self.display_conf.get("highlightThickness")
        self.frame_relief = self.display_conf.get("frameRelief")
        self.resizable = self.display_conf.get("resizable")

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
        self.root.bind("<KeyPress>", self.on_key_press)

        (
            self.tile_x,
            self.tile_y,
            self.font_width,
            self.font_height,
            self.body_width,
            self.body_height,
        ) = self.measure_font_size(self.font)

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
    def refresh_window(self):
        logger.debug("Refreshing window.")

        last_frame = []
        for widget in self.root.winfo_children():
            last_frame.append(widget)

        self.init_components()
        untitledHelper.destroy_listed_widgets(self, last_frame)

    ### Init Method ###
    def init_components(self):
        (
            self.tile_x,
            self.tile_y,
            self.font_width,
            self.font_height,
            self.body_width,
            self.body_height,
        ) = untitledHelper.measure_font_size(self.font)
        logger.debug(f"init_components - current_screen: {self.current_screen}")

        if self.current_screen == "title_screen":
            logger.debug("Loading title screen.")
            untitled_title = UntitledTitleScreen(self.root, self.conf)
            self.title_label = untitled_title.init_title_screen(
                self.font, self.bg, self.fg
            )
            untitled_title.load_title(
                self.title_label, self.window_width // 2, self.window_height // 2
            )

        elif self.current_screen == "main_menu":
            logger.debug("Loading main menu.")
            self.main_menu = main_menu(self.root, self.conf)
            self.current_screen = self.main_menu.init_menu()

        elif self.current_screen == "in_game":
            game_frames = self.init_frames(
                self.font_height, self.header_conf["pady"], self.footer_conf["pady"]
            )
            self.pack_game_frames(game_frames)


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

    def title_screen_key_press(self, event):
        if event.keysym:
            logger.debug("Go to main_menu - Key pressed: %s", event.keysym)
            self.current_screen = "main_menu"
            logger.debug(
                f"title_screen_key_press - current_screen: {self.current_screen}"
            )
            self.refresh_window()
