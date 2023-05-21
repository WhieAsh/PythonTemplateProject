import pytest
from app.create_app import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from models import recreate_postgres_tables


@pytest.fixture(scope="session")
def valid_full_profile_info() -> dict:
    full_profile_info = dict(short_description="This is short desc1",
                                        long_bio="This is very log bio",
                                        user_name="test_user",
                                        liked_posts=[1, 1, 1])

    return full_profile_info


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    recreate_postgres_tables()
    test_app = create_app()
    #test_client = TestClient(test_app)

    return test_app
