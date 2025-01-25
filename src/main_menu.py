
import sys, os
import tkinter as tk

loggerdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'loggers')
sys.path.append(loggerdir)

from untitled_logger import logger # type: ignore

class main_menu:
    def __init__(self, root, conf):
        self.root = root
        
        self.conf = conf
        self.menu_conf = conf['main_menu']
        
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

    def init_menu(self):
        logger.info('Initializing main menu text')
        
        for index, line in enumerate(self.menu):
            logger.debug(f'Init menu item {line["text"]}')
            
            self._init_title_label(index, line['state'])
            
            
    def _init_title_label(self, i, state):
        font_family = self.menu_conf[state]['fontFamily']
        font_size = self.menu_conf[state]['fontSize']
        font_weight = self.menu_conf[state]['fontWeight']
        
        font = (font_family, font_size, font_weight)
        
        fg = self.conf['colors'][self.menu_conf[state]['fg']]
        bg = self.conf['colors'][self.menu_conf[state]['bg']]
        
        self.title_label = tk.Label(
            self.root,
            text=self.menu[i]['text'],
            font=font,
            bg=bg,
            fg=fg
        )
        
        self.title_label.pack(pady=(self.conf['display']['framePadding'], 0))
            
    def new_game(self):
        logger.info('New game selected')
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
        pass