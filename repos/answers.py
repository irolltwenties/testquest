from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.dto import AnswerDTO
from models.orm import AnswerORM, QuestionORM
from repos.protocols import BaseRepository, IAnswersRepository


class AnswersRepository(BaseRepository[AnswerDTO, int], IAnswersRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AnswerDTO)

    async def get_by_id(self, answer_id: int) -> AnswerDTO | None:
        result = await self._session.execute(
            select(AnswerORM).where(AnswerORM.id == answer_id)
        )
        orm_obj = result.scalar_one_or_none()
        return AnswerDTO.model_validate(orm_obj) if orm_obj else None

    async def get_by_question_id(self, question_id: int) -> list[AnswerDTO]:
        result = await self._session.execute(
            select(AnswerORM).where(AnswerORM.question_id == question_id)
        )
        orm_objects = result.scalars().all()
        return [AnswerDTO.model_validate(orm_obj) for orm_obj in orm_objects]

    async def create(self, answer_data: dict) -> AnswerDTO:
        question_exists = await self._check_question_exists(answer_data["question_id"])
        if not question_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with id {answer_data['question_id']} not found",
            )

        # create answer
        orm_obj = AnswerORM(**answer_data)
        self._session.add(orm_obj)
        await self._session.flush()
        await self._session.refresh(orm_obj)
        return AnswerDTO.model_validate(orm_obj)

    async def _check_question_exists(self, question_id: int) -> bool:
        """returns false if not exists"""
        result = await self._session.execute(
            select(QuestionORM).where(QuestionORM.id == question_id)
        )
        return result.scalar_one_or_none() is not None

    async def delete(self, answer_id: int) -> bool:
        result = await self._session.execute(
            delete(AnswerORM).where(AnswerORM.id == answer_id)
        )
        await self._session.flush()
        return result.rowcount > 0
