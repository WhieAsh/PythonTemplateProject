from fastapi import FastAPI
from app.routes.users import create_user_router
from app.exception_hendlers import add_exception_handler
from app.clients.db import DatabaseClient
from app.config import Config


def create_app() -> FastAPI:

    new_app = FastAPI()
    config = Config()
    database_client = DatabaseClient(config, ["user", "liked_post"])
    new_app.include_router(create_user_router(database_client))
    add_exception_handler(new_app)

    return new_app
