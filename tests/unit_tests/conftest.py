
import pytest
from app.services.users import UserService
from app.schemas.users import FullProfileInfo
from app.clients.db import DatabaseClient
from app.config import Config
from models import recreate_postgres_tables
import pytest_asyncio
from models import User, LikedPost

from unittest.mock import AsyncMock


@pytest.fixture(scope="session")
def full_profile_info() -> FullProfileInfo:
    full_profile_info = FullProfileInfo(short_description="This is short desc1",
                                        long_bio="This is very log bio",
                                        user_name="test_user",
                                        liked_posts=[1, 1, 1])

    return full_profile_info


@pytest.fixture(scope="session")
def config() -> Config:
    return Config()


@pytest_asyncio.fixture()
async def database_client(config: Config) -> DatabaseClient:
    recreate_postgres_tables()
    db_client = DatabaseClient(config, ["user", "liked_post"])
    await db_client.database.connect()
    yield db_client
    await db_client.database.disconnect()


@pytest.fixture()
def user_service(database_client):
    user_service = UserService(database_client)
    return user_service


@pytest.fixture()
def mocking_database_client() -> DatabaseClient:
    mock = AsyncMock()
    mock.user = User.__table__
    mock.liked_post = LikedPost.__table__
    return mock


@pytest.fixture()
def mocking_user_service(mocking_database_client):
    user_service = UserService(mocking_database_client)
    return user_service
