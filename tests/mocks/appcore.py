from unittest.mock import AsyncMock

from app.сore import App
from app.logger import configure_logger
from config.config import Configuration
from tests.mocks.factory import FakeRepositoryFactory
from tests.mocks.gateway import FakeGateway


class FakeApp(App):
    def __init__(self, config: Configuration):
        self._logger = configure_logger("test-uvicorn-app")
        self.config = config
        self.gateway = FakeGateway(config)
        self.fastapi_app = self._create_fastapi_app()
        self._setup_routes()

    @staticmethod
    def get_repository_factory(gateway: FakeGateway) -> FakeRepositoryFactory:
        return gateway.get_repository_factory(AsyncMock())
