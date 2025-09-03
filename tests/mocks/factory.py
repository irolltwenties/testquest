from sqlalchemy.ext.asyncio import AsyncSession

from repos.factory import RepositoryFactory
from repos.protocols import IQuestionsRepository, IAnswersRepository
from tests.mocks.answers_repo import FakeAnswersRepository
from tests.mocks.questions_repo import FakeQuestionsRepository


class FakeRepositoryFactory(RepositoryFactory):
    __questions = FakeQuestionsRepository()
    __answers = FakeAnswersRepository(__questions)

    def __init__(self, session: AsyncSession):
        pass

    @property
    def questions(self) -> IQuestionsRepository:
        return self.__questions

    @property
    def answers(self) -> IAnswersRepository:
        return self.__answers
