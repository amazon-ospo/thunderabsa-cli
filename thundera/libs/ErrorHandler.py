import logging
from pathlib import Path


class ErrorHandler:

    def __init__(self, className):
        self.errorlog = []

        self.logger = logging.getLogger(className)

        c_handler = logging.StreamHandler()
        # f_handler = logging.StreamHandler()
        logpath = './thundera.log'
        filename = Path(logpath)
        filename.touch(exist_ok=True)
        f_handler = logging.FileHandler(logpath)
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.ERROR)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)

    def error(self, message):
        self.logger.error(message)
        # print(message)

    def info(self, message):
        self.logger.info(message)
        # print(message)
