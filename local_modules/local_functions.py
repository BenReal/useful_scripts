import os
import logging
import time

def configure_logging(log_file_path):
    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Open the log file with the desired encoding using FileHandler
    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the FileHandler to the root logger
    logging.getLogger('').addHandler(file_handler)
    logging.getLogger('').setLevel(logging.INFO)








