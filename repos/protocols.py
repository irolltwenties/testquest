from typing import Protocol, TypeVar, Generic, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from models.dto import QuestionDTO, AnswerDTO


T = TypeVar("T")
ID = TypeVar("ID")


class IRepository(Protocol[T, ID]):
    """Base repo interface"""

    async def get_by_id(self, id: ID) -> Optional[T]: ...

    async def get_all(self) -> list[T]: ...

    async def create(self, entity: T | Dict) -> T: ...

    async def update(self, entity: T) -> T: ...

    async def delete(self, id: ID) -> bool: ...


class IQuestionsRepository(IRepository[QuestionDTO, int], Protocol):
    # could skip this cause no special methods here
    pass


class IAnswersRepository(IRepository[AnswerDTO, int], Protocol):
    def get_by_question_id(self, question_id): ...


class BaseRepository(Generic[T, ID]):

    def __init__(self, session: AsyncSession, model: type[T]):
        self._session = session
        self._model = model
