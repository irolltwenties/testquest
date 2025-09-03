from datetime import datetime
from typing import List, Optional
from models.dto import QuestionDTO


class FakeQuestionsRepository:

    _shared_storage = {}
    _next_shared_id = 1

    def __init__(self):
        self._initialize_with_data()

    def _initialize_with_data(self):
        if not self._shared_storage:
            questions = [
                {"text": "Что такое Python?", "created_at": datetime.now()},
                {"text": "Как работает GIL?", "created_at": datetime.now()},
                {"text": "Что такое декораторы?", "created_at": datetime.now()},
            ]

            for question_data in questions:
                question = QuestionDTO(id=self._next_shared_id, **question_data)
                self._shared_storage[self._next_shared_id] = question
                self._next_shared_id += 1

    async def get_all(self) -> List[QuestionDTO]:
        return list(self._shared_storage.values())

    async def get_by_id(self, question_id: int) -> Optional[QuestionDTO]:
        return self._shared_storage.get(question_id)

    async def create(self, question_data: dict) -> QuestionDTO:
        question = QuestionDTO(
            id=self._next_shared_id,
            text=question_data["text"],
            created_at=datetime.now(),
        )
        self._shared_storage[self._next_shared_id] = question
        self._next_shared_id += 1
        return question

    async def delete(self, question_id: int) -> bool:
        if question_id in self._shared_storage:
            del self._shared_storage[question_id]
            return True
        return False

    @classmethod
    def reset_storage(cls):
        cls._shared_storage.clear()
        cls._next_shared_id = 1
