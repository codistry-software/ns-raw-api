import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        log_directory = "logs"
        os.makedirs(log_directory, exist_ok=True)
        log_file = os.path.join(log_directory, "app.log")

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger

logger = Logger().get_logger()
