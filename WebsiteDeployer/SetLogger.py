import logging


class LogSetter:
    def __init__(self, level: int):
        self.level = level
        self.format = '%(asctime)s - %(levelname)s - %(message)s'
        self.log_buffer = []

    def setup_logging(self):

        logger = logging.getLogger()
        logger.setLevel(level=self.level)

        logging.debug("Setting logging configuration...")

        logging.debug(f"Logging setup: Program-wide logging set to {logging.getLevelName(self.level)}")

        root_handler = logger.handlers[0]
        formatter = logging.Formatter(self.format)
        root_handler.setFormatter(formatter)

        logging.debug(f"Logging setup: Format set: {self.format}")

    def setup(self):
        self.setup_logging()
