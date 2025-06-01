#!/usr/bin/env python3
# Untitled Helper Module
# Aria Corona Feb 17th, 2025

import tkinter as tk
from tkinter import font
from functools import wraps
import json, os, pickle

class untitledHelper:
    def __init__(self, root):
        self.root = root
        self.logger = root.logger
        
    def create_frame(self, parent, bg, borderwidth, relief, **kwargs):
        """
        Creates a composite frame consisting of an outer border frame and an inner frame.
        Args:
            parent (tk.Widget): The parent widget to which the frames will be attached.
            bg (str): The background color for both the border and inner frames.
            borderwidth (int): The width of the border frame.
            relief (str): The type of relief to apply to the border frame (e.g., 'flat', 'raised', 'sunken', etc.).
            **kwargs: Additional keyword arguments to configure the frames.
        Returns:
            dict: A dictionary containing:
                - 'inner' (tk.Frame): The inner frame.
                - 'border' (tk.Frame): The outer border frame.
        """
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

    def measure_font_size(self, font_settings):
        """
        Measures the font size and calculates the number of tiles that can fit 
        within the body frame of the window.

        Args:
            font_settings (tuple): A tuple containing font settings:
                - font_settings[0] (str): The font family.
                - font_settings[1] (int): The font size.
                - font_settings[2] (str): The font weight.

        Returns:
            tuple: A tuple containing:
                - width (int): The width of a single character in pixels.
                - height (int): The height of a single character in pixels.
        """
        self.logger.debug("Measuring font size.")

        test_font = font.Font(
            family=font_settings[0], size=font_settings[1], weight=font_settings[2]
        )
        width = test_font.measure("W")  # Measure the width of a character
        height = test_font.metrics("linespace")  # Measure the height of a character
        self.logger.debug(f"Character size in pixels: {width}x{height}")

        body_height = (
            self.window_height
            - (height * 2)
            - (self.frame_pad * 3)
            - (self.border_thickness * 3)
        )
        body_width = self.window_width - self.frame_pad - self.border_thickness

        tile_x = body_width // width
        tile_y = body_height // height

        self.logger.debug(f"Tile size in characters: {tile_x}x{tile_y}")
        self.logger.debug(f"Body frame height: {body_height}")
        self.logger.debug(f"Body frame width: {body_width}")

        return width, height

    @staticmethod
    def clear_root(func):
        """
        Decorator to clear the root window of most common things.
        Destroys:
            - All child widgets
            - Unbinds all event types
            - Calls update_idletasks if available
        """
        def wrapper(self, *args, **kwargs):
            for widget in self.winfo_children():
                widget.destroy()
            for event in self.event_types:
                self.unbind(event)
            if hasattr(self, "update_idletasks"):
                self.update_idletasks()
            if hasattr(self, "logger"):
                self.logger.debug("Cleared root window.")
            return func(self, *args, **kwargs)

        return wrapper

    def load_json(self, path):
        """
        Loads a JSON file from the given path.
        
        Args:
            path (str): The path to the JSON file.
        
        Returns:
            dict: The loaded JSON data.
        """
        self.logger.debug(f"Loading JSON configuration from {path}")
        with open(path, 'r') as file:
            data = json.load(file)
        self.logger.debug("JSON configuration loaded successfully.")
        return data
    
    def save_json(self, data, path):
        """
        Saves data to a JSON file at the specified path.
        
        Args:
            data (dict): The data to save.
            path (str): The path where the JSON file will be saved.
        """
        self.logger.debug(f"Saving JSON configuration to {path}")
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
        self.logger.debug("JSON configuration saved successfully.")
        
    def load_pickle(self, path):
        """
        Loads a pickle file from the given path.
        Args:
            path (str): The path to the pickle file.
        Returns:
            object: The loaded data from the pickle file.
        """
        self.logger.debug(f"Loading pickle data from {path}")
        with open(path, 'rb') as file:
            data = pickle.load(file)
        self.logger.debug("Pickle data loaded successfully.")
        return data
    
    def save_pickle(self, data, path):
        """
        Saves data to a pickle file at the specified path.
        
        Args:
            data (object): The data to save.
            path (str): The path where the pickle file will be saved.
        """
        self.logger.debug(f"Saving pickle data to {path}")
        with open(path, 'wb') as file:
            pickle.dump(data, file)
        self.logger.debug("Pickle data saved successfully.")
        
    