from fastapi import FastAPI, Request
from app.exceptions import UserNotFound, UserAlreadyExists
from fastapi.responses import JSONResponse
import logging
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


def add_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(UserNotFound)
    async def exeption_hendler_user_not_found(request: Request, exc: UserNotFound):
        logger.error(f"User with {exc.user_id} does not existing")
        return JSONResponse(status_code=404, content={"message": "User does not exists", "user_id": exc.user_id})

    @app.exception_handler(UserAlreadyExists)
    async def exeption_hendler_user_already_exists(request: Request, exc: UserAlreadyExists):
        logger.error("Inserted user already exists")
        return JSONResponse(status_code=400, content={"message": "Inserted user already exists"})

    @app.exception_handler(IntegrityError)
    async def exeption_hendler_user_already_exists(request: Request, exc: IntegrityError):
        logger.error("User with this name already exists: {str(exc)}")
        return JSONResponse(status_code=400, content={"message": "User with this name already exists"})

    return None

