#!/usr/bin/env python3

import json, sys, os
import tkinter as tk
from tkinter import messagebox
from untitled_gameapp import Untgap

loggerdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'loggers')
sys.path.append(loggerdir)        

from untitled_logger import logger # type: ignore


# CONSTANTS
CONFIG_PATH = 'conf/conf.json'

# Load the JSON configuration file
def load_conf(path=CONFIG_PATH):
    logger.debug("Loading configuration from %s", path)
    
    with open(path, 'r') as config_file:
        config = json.load(config_file)
    
    logger.debug("Configuration loaded successfully.")
    return config

def main():
    
    root = tk.Tk()
    
    untgap = Untgap(
        root=root,
        conf_path = CONFIG_PATH
        )
    
    root.mainloop()
    pass

if __name__ == '__main__':
    main()
    pass