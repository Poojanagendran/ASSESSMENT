import logging


def logging_config(path):
    logging.basicConfig(
        filename=path,  # Log file name
        level=logging.INFO,  # Log level (INFO, DEBUG, WARNING, etc.)
        format='%(asctime)s - %(levelname)s - %(message)s')
