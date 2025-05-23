#!/usr/bin/env python3
# Aria Corona January 25th, 2025

import sys, os
import tkinter as tk

from loggers.untitled_logger import logger
from untitled_color import _reduce_brightness
from untitled_gameapp import Untgap


class MainMenu(Untgap):
    def __init__(self):
        if Untgap.current_screen != "main_menu":
            Untgap.init_components()

        self.conf = Untgap.conf
        self.color_conf = Untgap.conf["colors"]
        self.display_conf = Untgap.conf["display"]
        self.menu_conf = Untgap.conf["main_menu"]
        self.keybind_conf = Untgap.conf["keybinds"]

        self.menu = [
            {"text": "Untitled Rogue", "command": None, "state": "title"},
            {"text": "New Game", "command": self.new_game, "state": "selected"},
            {"text": "Load Game", "command": self.load_game, "state": "disabled"},
            {"text": "Options", "command": self.options, "state": "deselected"},
            {"text": "Quit", "command": self.quit_game, "state": "deselected"},
        ]

        self.sub_frame = None
        self.warning_menu = [
            {
                "text": "Yes",
                "command": self.new_game,
                "state": "deselected",
            },
            {
                "text": "No",
                "command": self.back_to_menu,
                "state": "selected",
            },
        ]

        self.check_for_save()

    def check_for_save(self):
        logger.info("Checking for save file")
        if os.path.exists("sav/save.json") and self.menu[2]["state"] == "disabled":
            self.menu[2]["state"] = "deselected"

    def handle_key_press(self, event):
        logger.debug(f"Key pressed: {event.keysym}")

        if event.keysym == self.keybind_conf["up"]:
            try:
                self.move_selection(-1)
            except IndexError:
                pass

        elif event.keysym == self.keybind_conf["down"]:
            try:
                self.move_selection(1)
            except IndexError:
                pass

        elif event.keysym == self.keybind_conf["button_1"]:
            self.select()

        elif event.keysym == self.keybind_conf["pause"]:
            self.jump_to_quit()

        return self.init_menu()

    def jump_to_quit(self):
        for line in self.menu:
            if line["state"] == "selected":
                line["state"] = "deselected"

            if line["text"] == "Quit":
                line["state"] = "selected"

    def select(self):
        for line in self.menu:
            if line["state"] == "selected":
                line["command"]()
                break

    def move_selection(self, direction):
        """
        Moves the selection in the menu based on the given direction.
        Args:
            direction (int): The direction to move the selection. Positive values move the selection down,
                             and negative values move the selection up.
        Logs:
            Logs the direction of the movement and the text of the new selection.
        Behavior:
            - If the new selection index is out of bounds, the function breaks.
            - If the new selection is 'disabled' or 'title', it recursively calls itself with an adjusted direction.
            - Updates the state of the current and new selection items.
        """
        logger.debug(f"Moving selection {direction}")

        for index, line in enumerate(self.menu):
            if line["state"] == "selected":
                if index + direction <= 0:
                    break

                logger.debug(f"Moving to: {self.menu[index+direction]['text']}")

                if self.menu[index + direction]["state"] in ["disabled", "title"]:
                    self.move_selection(direction + direction)
                    line["state"] = "deselected"
                    break

                self.menu[index + direction]["state"] = "selected"
                line["state"] = "deselected"
                break

    def init_menu(self):
        Untgap.destroy_all_widgets()
        
        logger.info("Initializing main menu text")
        for index, line in enumerate(self.menu):
            logger.debug(f'Init menu item {line["text"]}')
            self._init_menu_label(index, line["state"])

    def _init_menu_label(self, i, state):
        font_family = self.menu_conf[state]["fontFamily"]
        font_size = self.menu_conf[state]["fontSize"]
        font_weight = self.menu_conf[state]["fontWeight"]

        font = (font_family, font_size, font_weight)

        fg_base = self.conf["colors"][self.menu_conf[state]["fg"]]

        fg = _reduce_brightness(fg_base, self.menu_conf[state]["reduced"])
        bg = self.conf["colors"][self.menu_conf[state]["bg"]]

        # Create the label
        self.menu_label = tk.Label(
            Untgap.root, text=self.menu[i]["text"], font=font, bg=bg, fg=fg
        )

        # Position the title label
        if i == 0:
            y_position = Untgap.root.winfo_height() // 5

        # Position menu item labels
        else:
            padding = self.menu_conf["padding"]

            # Calculate the height of the menu
            menu_height = (len(self.menu) - 1) * (font_size + padding)

            # Center the menu in the window
            center = Untgap.root.winfo_height() // 2

            # Calculate the initial position
            init_pos = center - (menu_height // 2)

            # Calculate the position of the current menu item
            y_position = init_pos + ((font_size + padding) * (i - 1))

        # Center the title label and place
        self.menu_label.place(relx=0.5, y=y_position, anchor="center")

    def warning_overwrite_save(self):
        logger.info("Warning overwrite save")
        self.sub_screen = "warning_overwrite_save"
        label_text = "A save file already exists. Do you want to overwrite it?"
        choices = ["Yes", "No"]

    def back_to_menu(self):
        pass

    def new_game(self):
        logger.info("New game selected")

        if os.path.exists("sav/save.json"):
            if not self.warning_overwrite_save():
                return
        pass

    def load_game(self):
        logger.info("Load game selected")
        pass

    def options(self):
        logger.info("Options selected")
        pass

    def quit_game(self):
        logger.info("Quit game selected")
        Untgap.root.quit()
        Untgap.root.destroy()
        sys.exit(0)
        pass

    def run(self):
        logger.info("Running main menu")
        Untgap.root.bind("<KeyPress>", self.handle_key_press)
        self.init_menu()