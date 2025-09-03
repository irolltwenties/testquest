from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from pydantic import ValidationError

from repos.factory import RepositoryFactory
from repos.gateway import DatabaseGateway
from config.config import Configuration
from app.logger import configure_logger


class App:
    """Класс-обертка для FastAPI приложения"""

    def __init__(self, config: Configuration):
        self.config = config
        self._logger = configure_logger("uvicorn-app")
        self.gateway = DatabaseGateway(config)
        self.fastapi_app = self._create_fastapi_app()
        self._setup_routes()

    def _create_fastapi_app(self) -> FastAPI:
        """create instance of fastapi app"""

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self.gateway.initialize()
            yield
            await self.gateway.close()

        return FastAPI(
            title="Q&A API",
            description="API для вопросов и ответов",
            version="1.0.0",
            lifespan=lifespan,
        )

    def _setup_routes(self):
        """setup all endpoints routes"""
        router = APIRouter()  # one router but it could be two

        # Questions endpoints
        @router.get("/questions/", tags=["Questions"])
        async def get_all_questions(factory=self.get_repository_factory(self.gateway)):
            questions = await factory.questions.get_all()
            return questions

        @router.post("/questions/", tags=["Questions"])
        async def create_question(
            question_data: dict, factory=self.get_repository_factory(self.gateway)
        ):
            try:
                question = await factory.questions.create(question_data)
            except ValidationError as e:
                self._logger.exception(
                    "Validation error occurred during create_question"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return question

        @router.get("/questions/{question_id}", tags=["Questions"])
        async def get_question_with_answers(
            question_id: int, factory=self.get_repository_factory(self.gateway)
        ):
            question = await factory.questions.get_by_id(question_id)
            answers = await factory.answers.get_by_question_id(question_id)
            return {"question": question, "answers": answers}

        @router.delete("/questions/{question_id}", tags=["Questions"])
        async def delete_question(
            question_id: int, factory=self.get_repository_factory(self.gateway)
        ):
            try:
                success = await factory.questions.delete(question_id)
                return {"deleted": success}
            except Exception as e:
                self._logger.exception(
                    "Unexpected error occurred during delete_question"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )

        # Answers endpoints
        @router.post("/questions/{question_id}/answers/", tags=["Answers"])
        async def create_answer(
            question_id: int,
            answer_data: dict,
            factory=self.get_repository_factory(self.gateway),
        ):
            try:
                answer_data["question_id"] = question_id
                answer = await factory.answers.create(answer_data)
                return answer
            except HTTPException as e:
                self._logger.exception("Unexpected error occurred during create_answer")
                raise e
            except ValidationError as e:
                self._logger.exception("Validation error occurred during create_answer")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            except Exception as e:
                self._logger.exception("Unexpected error occurred during create_answer")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )

        @router.get("/answers/{answer_id}", tags=["Answers"])
        async def get_answer(
            answer_id: int, factory=self.get_repository_factory(self.gateway)
        ):
            answer = await factory.answers.get_by_id(answer_id)
            return answer

        @router.delete("/answers/{answer_id}", tags=["Answers"])
        async def delete_answer(
            answer_id: int, factory=self.get_repository_factory(self.gateway)
        ):
            success = await factory.answers.delete(answer_id)
            return {"deleted": success}

        self.fastapi_app.include_router(router)

    @property
    def app(self) -> FastAPI:
        return self.fastapi_app

    @staticmethod
    def get_repository_factory(gateway: DatabaseGateway) -> RepositoryFactory:

        async def _get_factory() -> RepositoryFactory:
            async with gateway.session() as session:
                factory = RepositoryFactory(session)
                yield factory

        return Depends(_get_factory)
