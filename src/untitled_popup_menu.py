#!/usr/bin/env python3
# Aria Corona February 7th, 2025

import sys, os, json
import tkinter as tk
from tkinter import font

from loggers.untitled_logger import logger

class popup_menu:
    def __init__(
        self, 
        root, 
        conf, 
        menu_options, 
        last_screen,
        header=None,
        xpos=None, 
        ypos=None, 
        width=None, 
        height=None, 
        padding=None,
        max_visible=None,
        start_pos=0,
        jump_to=None,
        header_font=None,
        deselect_font=None, 
        select_font=None, 
        disabled_font=None,
        leading=None,
        pack_propagate=False
    ):
        
        self.root = root
        self.last_screen = last_screen
        
        self.conf = conf
        self.popup_defaults = conf['pop_up_default']
        self.color_conf = conf['colors']
        self.display_conf = conf['display']
        self.menu_conf = conf['main_menu']
        self.keybind_conf =conf['keybinds']
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.padding = padding if padding else self.popup_defaults['padding']
        self.leading = leading if leading else self.popup_defaults['leading']
        self.pack_propagate = pack_propagate
        
        self.max_visible = max_visible if max_visible else self.popup_defaults['max_visible']
        
        self.menu = []
        self.header = header
        
        self.selected_font = select_font if select_font else self.popup_defaults['selected']
        self.deselected_font = deselect_font if deselect_font else self.popup_defaults['deselected']
        self.disabled_font = disabled_font if disabled_font else self.popup_defaults['disabled']
        self.header_font = header_font if header_font else self.popup_defaults['header']
        
        self.popup_frame = None
        
        for index, option in enumerate(menu_options):
            state = 'deselected'
            if index == start_pos:
                state = 'selected'
            
            self.menu.append({
                'text': option[0],
                'command': option[1],
                'state': state
            })
            
        if not self.menu:
            self.menu.append({
                'text': 'Close',
                'command': self.kill_popup,
                'state': 'selected'
            })
        
        # Set option for hitting the "b" button or cancel key in menu.
        if jump_to:
            self.jump_to_text = jump_to
        else:
            self.jump_to_text = self.menu[(len(self.menu)-1)]['text']
        

    
    def handle_keypress(self, event):
        pass
    
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
        logger.debug(f'Moving selection {direction}')
        
        for index, line in enumerate(self.menu):
            if line['state'] == 'selected':
                if index + direction <= 0:
                    break
                
                logger.debug(f'Moving to: {self.menu[index+direction]['text']}')
                
                if self.menu[index + direction]['state'] in ['disabled', 'title']:
                    self.move_selection(direction + direction)
                    line['state'] = 'deselected'
                    break
                    
                self.menu[index + direction]['state'] = 'selected'
                line['state'] = 'deselected'
                break
            
   
    def _check_pos_size(self):
        font_set = {self.selected_font, self.deselected_font, self.disabled_font}
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Autocalc missing frame width
        if not self.width:
            max_width = 0
            
            for set in font_set:
                family = set['fontFamily']
                size = set['fontSize']
                weight = set['fontWeight']
                current_font = (family, size, weight)
                
                tk_font = font.Font(font=current_font)
                
                for menu_item in self.menu:
                    width = tk_font.measure(menu_item['text'])

                    if width > max_width:
                        max_width = width

            raw_width = max_width + (self.popup_defaults['padding'] * 2)
            self.width = raw_width if raw_width < screen_width else screen_width
             
        # Autocalc missing frame height       
        if not self.height:
            menu_length = len(self.menu) if len(self.menu) < self.max_visible else self.max_visible
            
            max_size = 0
            for set in font_set:
                font_size = set['fontSize']
                max_size = max_size if font_size < max_size else font_size
            
            raw_height = (max_size * menu_length) + (self.popup_defaults['leading'] * (menu_length + 1))
            self.height = raw_height if raw_height < screen_height else screen_height
        
        # Center the frame if no position is given
        if not self.xpos:
            self.xpos = (screen_width - self.width) // 2  
        if not self.ypos:
            self.ypos = (screen_height - self.height) // 2
    
    
    def init_popup(self):
        logger.info(f"Initializing popup menu: {self.current_screen}.")
        
        self._check_pos_size()
        
        # Create the popup frame with the given width and height
        self.popup_frame = tk.Frame(self.root, width=self.width, height=self.height)
        self.popup_frame.place(x=self.xpos, y=self.ypos)
        self.popup_frame.pack_propagate(self.pack_propagate)  # Prevent the frame from resizing to fit its content
        
        # Add menu items to the frame
        for line in self.menu:
            label = tk.Label(self.popup_frame, text=line['text'], font=self.deselected_font)
            label.pack()
            if line['state'] == 'selected':
                label.config(font=self.selected_font)
            elif line['state'] == 'disabled':
                label.config(font=self.disabled_font)
        
    
    def kill_popup(self):
        logger.debug("Killing popup menu.")
        self.current_screen = self.last_screen
        if self.popup_frame:
            self.popup_frame.destroy()
        return self.last_screen
    
    
    def jump_to(self):
        original = self.menu[0]['text']
        
        for line in self.menu:
            if line['state'] == 'selected':
                original = line['text']
                line['state'] = 'deselected'
                
            if line['text'] == self.jump_to_text:
                line['state'] = 'selected'

        # If all items are deselected, select the first item
        if all(line['state'] == 'deselected' for line in self.menu):
            self.menu[0]['state'] = 'selected'
    
    
    def select(self):
        for line in self.menu:
            if line['state'] == 'selected':
                line['command']()