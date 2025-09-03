import pytest
from datetime import datetime
from pydantic import ValidationError

from models.dto import QuestionDTO, AnswerDTO


class TestQuestionDTO:
    def test_valid_question_creation(self):
        # Valid data
        question = QuestionDTO(id=1, text="Valid question", created_at=datetime.now())
        assert question.id == 1
        assert question.text == "Valid question"

    def test_invalid_question_raises_validation_error(self):
        # Invalid data - missing required field
        with pytest.raises(ValidationError):
            QuestionDTO(id=1)  # Missing text field

    def test_question_without_created_at_raises_error(self):
        # created_at is required
        with pytest.raises(ValidationError):
            QuestionDTO(id=1, text="Test")  # Missing created_at

    def test_validate_not_empty_text(self):
        with pytest.raises(ValidationError):
            QuestionDTO(id=1, text="", created_at=datetime.now())

        with pytest.raises(ValidationError):
            QuestionDTO(id=1, text="     ", created_at=datetime.now())


class TestAnswerDTO:
    def test_valid_answer_creation(self):
        answer = AnswerDTO(
            id=1,
            question_id=1,
            user_id="user1",
            text="Test answer",
            created_at=datetime.now(),
        )
        assert answer.question_id == 1
        assert answer.user_id == "user1"

    def test_answer_missing_required_fields(self):
        with pytest.raises(ValidationError):
            AnswerDTO(id=1)  # Missing all required fields

    def test_validate_non_empty_vals(self):
        with pytest.raises(ValidationError):
            AnswerDTO(
                id=1,
                question_id=1,
                user_id="",
                text="valid text",
                created_at=datetime.now(),
            )

        with pytest.raises(ValidationError):
            AnswerDTO(
                id=1,
                question_id=1,
                user_id="valid id",
                text="",
                created_at=datetime.now(),
            )

        with pytest.raises(ValidationError):
            AnswerDTO(
                id=1, question_id=1, user_id="", text="", created_at=datetime.now()
            )

        with pytest.raises(ValidationError):
            AnswerDTO(
                id=1, question_id=1, user_id=" ", text="", created_at=datetime.now()
            )

            with pytest.raises(ValidationError):
                AnswerDTO(
                    id=1,
                    question_id=1,
                    user_id="",
                    text="   ",
                    created_at=datetime.now(),
                )
