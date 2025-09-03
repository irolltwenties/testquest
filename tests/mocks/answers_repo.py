from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status

from models.dto import AnswerDTO


class FakeAnswersRepository:
    """test repo to check app logics"""

    def __init__(self, questions_repository):
        self._storage = {}  # {id: AnswerDTO}
        self._next_id = 1
        self.questions_repo = questions_repository
        self._initialize_with_data()

    def _initialize_with_data(self):
        """initial test data"""
        answers = [
            {
                "question_id": 1,
                "user_id": "user1",
                "text": "Python - это язык программирования",
            },
            {"question_id": 1, "user_id": "user2", "text": "Интерпретируемый язык"},
            {"question_id": 2, "user_id": "user1", "text": "Global Interpreter Lock"},
        ]

        for answer_data in answers:
            answer = AnswerDTO(
                id=self._next_id, **answer_data, created_at=datetime.now()
            )
            self._storage[self._next_id] = answer
            self._next_id += 1

    async def get_by_id(self, answer_id: int) -> Optional[AnswerDTO]:
        return self._storage.get(answer_id)

    async def get_by_question_id(self, question_id: int) -> List[AnswerDTO]:
        return [
            answer
            for answer in self._storage.values()
            if answer.question_id == question_id
        ]

    async def create(self, answer_data: dict) -> AnswerDTO:
        question = await self.questions_repo.get_by_id(answer_data["question_id"])
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with id {answer_data['question_id']} not found",
            )

        answer = AnswerDTO(
            id=self._next_id,
            question_id=answer_data["question_id"],
            user_id=answer_data["user_id"],
            text=answer_data["text"],
            created_at=datetime.now(),
        )

        self._storage[self._next_id] = answer
        self._next_id += 1
        return answer

    async def delete(self, answer_id: int) -> bool:
        if answer_id in self._storage:
            del self._storage[answer_id]
            return True
        return False
