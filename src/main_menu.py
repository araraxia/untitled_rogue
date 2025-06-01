#!/usr/bin/env python3
# Aria Corona January 25th, 2025

import sys, os, json
import tkinter as tk

from src.untitled_color import _reduce_brightness
from src.untitled_sounds import UntitledSounds

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.update()
        self.logger = self.root.logger
        self.conf = self.root.config
        self.load_conf()
        self.keybind_conf = self.conf.get("keybinds", {})

        self.menu = [
            {"text": "Untitled Rogue", "command": None, "state": "title", "label": None},
            {"text": "New Game", "command": self.new_game, "state": "selected", "label": None},
            {"text": "Load Game", "command": self.load_game, "state": "disabled", "label": None},
            {"text": "Options", "command": self.options, "state": "deselected", "label": None},
            {"text": "Quit", "command": self.quit_game, "state": "deselected", "label": None},
        ]

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
        self.init_menu()

    def load_conf(self):
        self.logger.info("Loading main menu configuration")
        with open("conf/main_menu_conf.json", "r") as file:
            self.menu_conf = json.load(file)
        self.logger.debug(f"Menu configuration loaded: {self.menu_conf}")

    def check_for_save(self):
        self.logger.info("Checking for save file")
        if os.path.exists("sav/save.json") and self.menu[2]["state"] == "disabled":
            self.menu[2]["state"] = "deselected"

    def init_menu(self):
        self.logger.info("Initializing main menu text")
        self.load_sounds()
        for index, line in enumerate(self.menu):
            self.logger.debug(f'Init menu item {line["text"]}')
            self._init_menu_label(index, line["state"])
        self.root.bind("<KeyPress>", self.on_key_press)
        self.logger.info("Main menu initialized")

    def load_sounds(self):
        self.logger.info("Loading sounds for main menu")
        self.sounds = {
            "menu_index_error": UntitledSounds(self.root, "menu_index_error"),
            "menu_change_index": UntitledSounds(self.root, "menu_change_index"),
            "menu_select": UntitledSounds(self.root, "menu_select"),
            "menu_back": UntitledSounds(self.root, "menu_back"),
        }

    def _init_menu_label(self, i, state):
        font_family = self.menu_conf[state]["fontFamily"]
        font_size = self.menu_conf[state]["fontSize"]
        font_weight = self.menu_conf[state]["fontWeight"]

        font = (font_family, font_size, font_weight)

        fg_base = self.menu_conf.get(state, {}).get("fg", "#FFFFFF")

        fg = _reduce_brightness(fg_base, self.menu_conf[state]["reduced"])
        bg = self.menu_conf.get(state, {}).get("bg", "#000000")

        # Create the label
        self.menu_label = tk.Label(
            self.root, text=self.menu[i]["text"], font=font, bg=bg, fg=fg
        )

        # Position the title label
        if i == 0:
            y_position = self.root.winfo_height() // 5

        # Position menu item labels
        else:
            padding = self.menu_conf["padding"]

            # Calculate the height of the menu
            menu_height = (len(self.menu) - 1) * (font_size + padding)

            # Center the menu in the window
            center = self.root.winfo_height() // 2

            # Calculate the initial position
            init_pos = center - (menu_height // 2)

            # Calculate the position of the current menu item
            y_position = init_pos + ((font_size + padding) * (i - 1))

        # Center the title label and place
        self.menu[i]["label"] = self.menu_label
        self.menu_label.place(relx=0.5, y=y_position, anchor="center")


    # Event Handlers

    def on_key_press(self, event):
        self.logger.debug(f"Key pressed: {event.keysym}")

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

        return

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
        self.logger.debug(f"Moving selection {direction}")

        for index, line in enumerate(self.menu):
            go_to = index + direction
            if line.get("state") == "selected":
                # If the next index is out of bounds, sound and break
                if 0 > go_to or go_to >= len(self.menu):
                    self.root.play_sound(self.sounds.get("menu_index_error"))
                    break
                
                next_text = self.menu[go_to].get("text")
                next_state = self.menu[go_to].get("state")

                # If the next state is 'disabled' or 'title', skip to the next item
                if next_state in ["disabled", "title"]:
                    self.move_selection(direction + direction)
                    break
               
                # Play sound for changing index
                self.root.play_sound(self.sounds.get("menu_change_index"))
                
                # Get the current and next labels and their foreground colors
                current_label = line.get("label")
                current_fg = self.menu_conf.get("deselected", {}).get("fg", "#FFFFFF")
                current_fg = _reduce_brightness(current_fg, self.menu_conf["deselected"]["reduced"])
                
                next_label = self.menu[go_to].get("label")
                next_fg = self.menu_conf.get("selected", {}).get("fg", "#FFFFFF")
                next_fg = _reduce_brightness(next_fg, self.menu_conf["selected"]["reduced"])
                
                self.logger.debug(f"Moving to: {next_text} (state: {next_state})")
                
                # Update the state of the current and next menu items
                self.menu[go_to]["state"] = "selected"
                next_label.config(
                    fg=next_fg,
                    bg=self.menu_conf.get("selected", {}).get("bg", "#000000"),
                    font=(
                        self.menu_conf["selected"]["fontFamily"],
                        self.menu_conf["selected"]["fontSize"],
                        self.menu_conf["selected"]["fontWeight"]
                    )
                )
                
                self.menu[index]["state"] = "deselected"
                current_label.config(
                    fg=current_fg,
                    bg=self.menu_conf.get("deselected", {}).get("bg", "#000000"),
                    font=(
                        self.menu_conf["deselected"]["fontFamily"],
                        self.menu_conf["deselected"]["fontSize"],
                        self.menu_conf["deselected"]["fontWeight"]
                    )
                )
                break


    
    # Menu Action Methods

    def back_to_menu(self):
        pass

    def new_game(self):
        self.logger.info("New game selected")

        if os.path.exists("sav/save.json"):
            if not self.warning_overwrite_save():
                return
        self.root.current_window = "char_creation"
        
        pass

    def load_game(self):
        self.logger.info("Load game selected")
        pass

    def options(self):
        self.logger.info("Options selected")
        pass

    def quit_game(self):
        self.logger.info("Quit game selected")
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
        pass
    
    def warning_overwrite_save(self):
        self.logger.info("Warning overwrite save")
        self.sub_screen = "warning_overwrite_save"
        label_text = "A save file already exists. Do you want to overwrite it?"
        choices = ["Yes", "No"]

