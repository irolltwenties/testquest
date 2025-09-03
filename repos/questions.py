from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.dto import QuestionDTO
from models.orm import QuestionORM
from repos.protocols import BaseRepository, IQuestionsRepository


class QuestionsRepository(BaseRepository[QuestionDTO, int], IQuestionsRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, QuestionDTO)

    async def get_all(self) -> list[QuestionDTO]:
        result = await self._session.execute(select(QuestionORM))
        orm_objects = result.scalars().all()
        return [QuestionDTO.model_validate(orm_obj) for orm_obj in orm_objects]

    async def get_by_id(self, question_id: int) -> QuestionDTO | None:
        result = await self._session.execute(
            select(QuestionORM).where(QuestionORM.id == question_id)
        )
        orm_obj = result.scalar_one_or_none()
        return QuestionDTO.model_validate(orm_obj) if orm_obj else None

    async def create(self, question_data: dict) -> QuestionDTO:
        orm_obj = QuestionORM(**question_data)
        self._session.add(orm_obj)
        await self._session.flush()
        await self._session.refresh(orm_obj)
        return QuestionDTO.model_validate(orm_obj)

    async def delete(self, question_id: int) -> bool:
        # check existence
        question = await self.get_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with id {question_id} not found",
            )

        result = await self._session.execute(
            delete(QuestionORM).where(QuestionORM.id == question_id)
        )
        await self._session.flush()
        return result.rowcount > 0
