import os

import os
import logging
from abc import ABC
from typing import List
from dotenv import load_dotenv

logging.basicConfig()
Logger = logging.getLogger()


def load_env_variables():
    load_dotenv("../.env")
    load_dotenv(".env")
    load_dotenv("env")
    load_dotenv("app/docker.env")
    load_dotenv("docker.env")


load_env_variables()


class Settings(ABC):
    def __init__(self):
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE")
        self.logger = self.setup_logger_level()

    def setup_logger_level(self) -> logging.Logger:
        if self.LOG_LEVEL == "DEBUG":
            Logger.setLevel(logging.DEBUG)
        else:
            Logger.setLevel(logging.INFO)
        return Logger


class AppSettings(Settings):
    def __init__(self):
        super().__init__()
        self.APP_HOST = os.getenv("APP_HOST")
        self.APP_PORT = int(os.getenv("APP_PORT"))
        self.logger.debug(self.__dict__)

    @property
    def attribute_extraction_app_server(self) -> str:
        return self.SERVER_APP_HOST + ":" + self.SERVER_APP_PORT

