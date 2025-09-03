"""Initial data

Revision ID: 46e618420179
Revises: a86eb932cfe1
Create Date: 2025-09-02 20:33:27.052515

"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "46e618420179"
down_revision: Union[str, Sequence[str], None] = "a86eb932cfe1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    questions_table = sa.Table(
        "questions",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("text", sa.String),
        sa.Column("created_at", sa.DateTime),
    )

    answers_table = sa.Table(
        "answers",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("question_id", sa.Integer),
        sa.Column("user_id", sa.String),
        sa.Column("text", sa.String),
        sa.Column("created_at", sa.DateTime),
    )

    op.bulk_insert(
        questions_table,
        [
            {
                "text": "Что такое Python и каковы его основные преимущества?",
                "created_at": datetime.utcnow(),
            },
            {
                "text": "Как работает garbage collection в Python?",
                "created_at": datetime.utcnow(),
            },
            {
                "text": "В чем разница между списками и кортежами в Python?",
                "created_at": datetime.utcnow(),
            },
            {
                "text": "Что такое декораторы в Python и как их использовать?",
                "created_at": datetime.utcnow(),
            },
            {
                "text": "Как работает наследование в Python?",
                "created_at": datetime.utcnow(),
            },
        ],
    )

    op.bulk_insert(
        answers_table,
        [
            {
                "question_id": 1,
                "user_id": "user1",
                "text": "Python - это интерпретируемый язык программирования высокого уровня. Его преимущества: читаемость кода, большое сообщество, богатая экосистема библиотек.",
                "created_at": datetime.utcnow(),
            },
            {
                "question_id": 1,
                "user_id": "user2",
                "text": "Основные преимущества: динамическая типизация, автоматическое управление памятью, кроссплатформенность.",
                "created_at": datetime.utcnow(),
            },
            {
                "question_id": 2,
                "user_id": "user3",
                "text": "В Python используется reference counting и generational garbage collection для автоматического управления памятью.",
                "created_at": datetime.utcnow(),
            },
            {
                "question_id": 3,
                "user_id": "user1",
                "text": "Списки изменяемы (mutable), а кортежи неизменяемы (immutable). Списки используют квадратные скобки [], кортежи - круглые ().",
                "created_at": datetime.utcnow(),
            },
            {
                "question_id": 4,
                "user_id": "user4",
                "text": "Декораторы - это функции, которые модифицируют поведение других функций. Используются с синтаксисом @decorator_name.",
                "created_at": datetime.utcnow(),
            },
            {
                "question_id": 5,
                "user_id": "user2",
                "text": "Python поддерживает множественное наследование. Классы наследуют методы и атрибуты от родительских классов.",
                "created_at": datetime.utcnow(),
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM answers")
    op.execute("DELETE FROM questions")

    op.execute("ALTER SEQUENCE questions_id_seq RESTART WITH 1")
    op.execute("ALTER SEQUENCE answers_id_seq RESTART WITH 1")
