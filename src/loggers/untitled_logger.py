#!/usr/bin/env python3

import logging
import os

logs_dir = 'logs'
info_file = 'untitled_info.log'
error_file = 'untitled_error.log'

# Create the logs directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

info_path = os.path.join(logs_dir, info_file)
error_path = os.path.join(logs_dir, error_file)

# Create logger
logger = logging.getLogger('shared_logger')
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Create handlers
info_handler = logging.FileHandler(info_path)
error_handler = logging.FileHandler(error_path)
debug_handler = logging.StreamHandler()

# Set levels for handlers
info_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)
debug_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(debug_handler)

