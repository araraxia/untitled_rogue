#!/usr/bin/env python3
# Aria Corona

from src.untitled_helper import untitledHelper
import tkinter as tk
import json

class UntitledTitleScreen():
    def __init__(self, root, conf, log):
        self.root = root
        self.root.update()
        self.log = log
        self.conf = conf
        self.init_conf()
        self.init_title_screen()
        
    def load_title(self):
        x = self.root.winfo_width() / 2
        y = (self.root.winfo_height() / 3)
        sy = y + (self.root.winfo_height() / 6)
    
        self.log.debug(f"Setting title screen position: x={x}, y={y}, sy={sy}")
    
        self.title_label.place(x=x, y=y, anchor="center") 
        self.subtitle_label.place(x=x, y=sy, anchor="center")
        self.root.bind("<Key>", self.on_key_press)
        
        self.log.debug("Title screen loaded and waiting for interaction.")
        
    def init_conf(self, conf_path="conf/title_conf.json"):
        self.log.debug(f"Loading configuration from {conf_path}")
        with open(conf_path, 'r') as file:
            conf = json.load(file)
        self.title_conf = conf
        
    def init_title_screen(self): 
        self.log.debug("init title screen")
        
        self.tt = self.title_conf.get("title_text")
        self.tst = self.title_conf.get("title_subtext")
        
        text_big = self.tt.get("text", "Missing Title Conf")
        text_small = self.tst.get("text", "Err")
        
        text_fg = self.conf.get("colors", {}).get("foreground", "#FFFFFF")
        text_bg = self.conf.get("colors", {}).get("background", "#000000")
        
        root_width = self.root.winfo_width()
        title_size = int(root_width * 0.75 / len(text_big))
        subtitle_size = int(root_width * 0.6 / len(text_small))
        
        title_font = (
            self.tt.get("fontFamily"),
            title_size,
            self.tt.get("fontWeight")
        )
         
        subtitle_font = (
            self.tst.get("fontFamily"),
            subtitle_size,
            self.tst.get("fontWeight")
        )

        self.title_label = tk.Label(self.root,
                                    text=text_big,
                                    font=title_font,
                                    bg=text_bg,
                                    fg=text_fg)
        
        self.subtitle_label = tk.Label(self.root,
                                       text=text_small,
                                       font=subtitle_font,
                                       bg=text_bg,
                                       fg=text_fg)
        
    def on_key_press(self, event):
        self.log.debug(f"Key pressed: {event.keysym}")
