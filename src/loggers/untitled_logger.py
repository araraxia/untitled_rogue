
import logging, os
from logging.handlers import TimedRotatingFileHandler

def setup_logger():
    logs_dir = 'logs'
    log_name = 'untitled.log'

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_path = os.path.join(logs_dir, log_name)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s')
    file_handler = TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    
    logger = logging.getLogger('Untitled')
    
    logger.handlers = []
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    
    logger.propagate = False
    logger.debug("logger initialized")
    
    return logger