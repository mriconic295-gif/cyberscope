"""
=========================================================
CyberScope Logger
Author : Krunal Paliwal
Version : 2.0
=========================================================
"""

from __future__ import annotations

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


class Logger:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance._initialize()

        return cls._instance

    def _initialize(self):

        log_dir = Path("logs")

        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "cyberscope.log"

        self.logger = logging.getLogger("CyberScope")

        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return

        formatter = logging.Formatter(

            "[%(asctime)s] "

            "[%(levelname)s] "

            "%(message)s",

            "%Y-%m-%d %H:%M:%S"

        )

        file_handler = RotatingFileHandler(

            log_file,

            maxBytes=5 * 1024 * 1024,

            backupCount=5,

            encoding="utf-8"

        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

        self.logger.addHandler(console_handler)

    # -------------------------------------------------

    def debug(self, message):

        self.logger.debug(message)

    def info(self, message):

        self.logger.info(message)

    def warning(self, message):

        self.logger.warning(message)

    def error(self, message):

        self.logger.error(message)

    def critical(self, message):

        self.logger.critical(message)

    def exception(self, message):

        self.logger.exception(message)


logger = Logger()


if __name__ == "__main__":

    logger.info("CyberScope Logger Started")

    logger.warning("Logger Test")

    logger.error("Logger Error Test")
