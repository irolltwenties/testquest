import datetime
from pydantic import BaseModel, Field, field_validator


class QuestionDTO(BaseModel):
    id: int
    text: str = Field(..., min_length=1, max_length=1000, pattern=r"^.*\S.*$")
    created_at: datetime.datetime

    class Config:
        from_attributes = True

    @field_validator("text")
    def validate_text_not_empty(cls, v):
        if not v or v.isspace():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class AnswerDTO(BaseModel):
    id: int
    question_id: int
    user_id: str = Field(..., min_length=1, max_length=100, pattern=r"^.*\S.*$")
    text: str = Field(..., min_length=1, max_length=5000, pattern=r"^.*\S.*$")
    created_at: datetime.datetime

    class Config:
        from_attributes = True

    @field_validator("user_id", "text")
    def validate_fields_not_empty(cls, v, field):
        if not v or v.isspace():
            raise ValueError(f"{field.name} cannot be empty or whitespace only")
        return v.strip()
