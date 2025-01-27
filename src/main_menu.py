#!/usr/bin/env python3
# Aria Corona January 25th, 2025

import sys, os
import tkinter as tk

loggerdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'loggers')
sys.path.append(loggerdir)

from untitled_logger import logger # type: ignore
from untitled_color import _reduce_brightness

class main_menu:
    def __init__(self, root, conf):
        self.root = root
        self.current_screen = "main_menu"
        self.sub_screen = ""

        
        self.conf = conf
        self.color_conf = conf['colors']
        self.display_conf = conf['display']
        self.menu_conf = conf['main_menu']
        self.keybind_conf = conf['keybinds']
        
        self.menu = [
            {
                'text': 'Untitled Rogue',
                'command': None,
                'state': 'title'
            },
            {
                'text': 'New Game',
                'command': self.new_game,
                'state': 'selected'
            },
            {
                'text': 'Load Game',
                'command': self.load_game,
                'state': 'disabled'
            },
            {
                'text': 'Options',
                'command': self.options,
                'state': 'deselected'
            },
            {
                'text': 'Quit',
                'command': self.quit_game,
                'state': 'deselected'
            }
        ]
        
        self.sub_frame = None
        self.warning_menu = [
            {
                'text': 'Yes',
                'command': self.new_game,
                'state': 'deselected',
            },
            {
                'text': 'No',
                'command': self.back_to_menu,
                'state': 'selected',
            }
        ]
        
        self.check_for_save()
    
    
    def check_for_save(self):
        logger.info('Checking for save file')
        if os.path.exists('sav/save.json') and self.menu[2]['state'] == 'disabled':
            self.menu[2]['state'] = 'deselected'
    
    
    def handle_key_press(self, event):
        logger.debug(f'Key pressed: {event.keysym}')
        
        if event.keysym == self.keybind_conf['up']:
            try:
                self.move_selection(-1)
            except IndexError:
                pass
            
        elif event.keysym == self.keybind_conf['down']:
            try:
                self.move_selection(1)
            except IndexError:  
                pass
            
        elif event.keysym == self.keybind_conf['button_1']:
            self.select()
            
        elif event.keysym == self.keybind_conf['pause']:
            self.jump_to_quit()
        
        return self.init_menu()
    
    
    def jump_to_quit(self):
        for line in self.menu:
            if line['state'] == 'selected':
                line['state'] = 'deselected'
                
            if line['text'] == 'Quit':
                line['state'] = 'selected'
    
    def select(self):
        for line in self.menu:
            if line['state'] == 'selected':
                line['command']()
                break
    
    def move_selection(self, direction):
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
    
    def init_menu(self):
        logger.info('Initializing main menu text')
        
        for widget in self.root.winfo_children():
            logger.debug(f'Destroying widget: {widget}')
            widget.destroy()
        
        for index, line in enumerate(self.menu):
            logger.debug(f'Init menu item {line["text"]}')
            
            self._init_menu_label(index, line['state'])
            
        return self.current_screen
            
    def _init_menu_label(self, i, state):
        font_family = self.menu_conf[state]['fontFamily']
        font_size = self.menu_conf[state]['fontSize']
        font_weight = self.menu_conf[state]['fontWeight']
        
        font = (font_family, font_size, font_weight)
        
        fg_base = self.conf['colors'][self.menu_conf[state]['fg']]
        
        fg = _reduce_brightness(fg_base, self.menu_conf[state]['reduced'])
        bg = self.conf['colors'][self.menu_conf[state]['bg']]
        
        # Create the label
        self.menu_label = tk.Label(
            self.root,
            text=self.menu[i]['text'],
            font=font,
            bg=bg,
            fg=fg
        )
        
        # Position the title label
        if i == 0:
            y_position = self.root.winfo_height() // 5
        
        # Position menu item labels
        else:
            padding = self.menu_conf['padding']

            # Calculate the height of the menu
            menu_height = (len(self.menu) - 1) * (font_size + padding)
            
            # Center the menu in the window
            center = self.root.winfo_height() // 2
            
            # Calculate the initial position
            init_pos = center - (menu_height // 2)
            
            # Calculate the position of the current menu item         
            y_position = init_pos + ((font_size + padding) * (i - 1))
            
        # Center the title label and place
        self.menu_label.place(relx=0.5, y=y_position, anchor='center')
            
    def warning_overwrite_save(self):
        logger.info('Warning overwrite save')
        self.sub_screen = "warning_overwrite_save"
        label_text = "A save file already exists. Do you want to overwrite it?"
        choices = ["Yes", "No"]
        
        warning_frames = self.create_warning_frame()
        
    
    def create_warning_frame(self):
        frame_size = (self.root.winfo_width() // 4, self.root.winfo_height() // 4)
        border_frame = (tk.Frame(self.root,
                                width=frame_size[0],
                                height=frame_size[1],
                                bg=self.color_conf['frame'],
                                borderwidth=self.display_conf['highlightThickness'],
                                relief=self.display_conf['frameRelief']
                                ))
        
        inner_frame = (tk.Frame(
            self.root,
            width=frame_size[0],
            height=frame_size[1],
            bg=self.color_conf['background']
            ))
        
        return (inner_frame, border_frame)
    
    def new_game(self):
        logger.info('New game selected')
        
        if os.path.exists('sav/save.json'):
            if not self.warning_overwrite_save():
                return
        pass
    
    def load_game(self):
        logger.info('Load game selected')
        pass
    
    def options(self):
        logger.info('Options selected')
        pass
    
    def quit_game(self):
        logger.info('Quit game selected')
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
        pass