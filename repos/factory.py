from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine

from repos.answers import AnswersRepository
from repos.protocols import IQuestionsRepository, IAnswersRepository
from repos.questions import QuestionsRepository
from config.config import Configuration


class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.__questions = QuestionsRepository(session)
        self.__answers = AnswersRepository(session)

    @property
    def questions(self) -> IQuestionsRepository:
        return self.__questions

    @property
    def answers(self) -> IAnswersRepository:
        return self.__answers


def get_async_engine(config: Configuration) -> AsyncEngine:
    return create_async_engine(
        "postgresql+asyncpg://"
        + f"{config.db_login}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}",
        echo=True,
        pool_size=20,
        max_overflow=20,
    )
