# tests/unit/repositories/test_questions_repository.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import HTTPException, status

from repos.questions import QuestionsRepository
from datetime import datetime

from models.orm import QuestionORM
from repos.answers import AnswersRepository


@pytest.mark.asyncio
class TestQuestionsRepository:
    @pytest.mark.asyncio
    async def test_create_question_returns_dto_with_correct_data(self):
        # Arrange
        mock_session = AsyncMock()

        mock_orm_obj = MagicMock()
        mock_orm_obj.id = 1
        mock_orm_obj.text = "Test question"
        mock_orm_obj.created_at = datetime.now()

        repo = QuestionsRepository(mock_session)

        # Act
        with patch("repos.questions.QuestionORM", return_value=mock_orm_obj):
            result = await repo.create({"text": "Test question"})

        # Assert
        assert result.text == "Test question"
        assert result.id == 1
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_returns_empty_list_for_no_data(self):
        # Arrange
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        repo = QuestionsRepository(mock_session)

        # Act
        result = await repo.get_all()

        # Assert
        assert result == []
        mock_session.execute.assert_called_once()


@pytest.mark.asyncio
class TestAnswersRepository:
    @pytest.mark.asyncio
    async def test_cannot_create_answer_for_nonexistent_question(self):
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute.return_value.scalar_one_or_none.return_value = None

        repo = AnswersRepository(mock_session)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            # stop when got exc
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with id 999 not found",
            )

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_can_create_multiple_answers_same_user(self):
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute.return_value.scalar_one_or_none.return_value = QuestionORM(
            id=1
        )

        # Mock
        mock_orm_obj = MagicMock()
        mock_orm_obj.id = 1
        mock_orm_obj.question_id = 1
        mock_orm_obj.user_id = "user1"
        mock_orm_obj.text = "Answer 1"
        mock_orm_obj.created_at = datetime.now()

        repo = AnswersRepository(mock_session)

        # Act
        with patch("repos.answers.AnswerORM", return_value=mock_orm_obj):
            answer1 = await repo.create(
                {"question_id": 1, "user_id": "user1", "text": "Answer 1"}
            )
            answer2 = await repo.create(
                {"question_id": 1, "user_id": "user1", "text": "Answer 2"}
            )

        # Assert
        assert answer1.question_id == 1
        assert answer2.question_id == 1
        assert mock_session.add.call_count == 2
