from os import getenv


class Configuration:
    def __init__(self):
        self.__host = getenv("TEST_QUEST_API_HOST", "0.0.0.0")
        self.__port = getenv("TEST_QUEST_API_PORT", "8000")
        self.__db_login = getenv("TEST_QUEST_DB_LOGIN", "")
        self.__db_password = getenv("TEST_QUEST_DB_PASSWORD", "")
        self.__db_name = getenv("TEST_QUEST_DB_NAME", "")
        self.__db_host = getenv("TEST_QUEST_DB_HOST", "")
        self.__db_port = getenv("TEST_QUEST_DB_PORT", "")

        for name, val in self.__dict__.items():
            if val == "":
                raise ValueError(f"Missing config for {name[1:]}")

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def db_login(self) -> str:
        return self.__db_login

    @property
    def db_password(self) -> str:
        return self.__db_password

    @property
    def db_name(self) -> str:
        return self.__db_name

    @property
    def db_host(self) -> str:
        return self.__db_host

    @property
    def db_port(self) -> str:
        return self.__db_port
