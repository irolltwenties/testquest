from os import getenv

from config.config import Configuration


class FakeConfiguration(Configuration):
    def __init__(self):
        self.__host = "0.0.0.0"
        self.__port = "8000"
        self.__db_login = "dev"
        self.__db_password = "dev"
        self.__db_name = "dev"
        self.__db_host = "localhost"
        self.__db_port = "5432"
