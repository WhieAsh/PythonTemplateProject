from fastapi import APIRouter, HTTPException, Depends
from app.services.users import UserService
from app.dependensies import rete_limit_check
from app.schemas.users import FullProfileInfo, UserProfileInfo, FullProfileInfos, CreateUserResponse
import logging
from fastapi.responses import Response
from fastapi import status
from app.clients.db import DatabaseClient

loger = logging.getLogger(__name__)


def create_user_router(database_client: DatabaseClient) -> APIRouter:
    user_router = APIRouter(
        prefix="/user",
        tags=["users"],
        dependencies=[Depends(rete_limit_check)]
    )
    users_service = UserService(database_client)

    @user_router.get("/dummy")
    async def get_dummy() -> Response:
        resource = Response()
        resource.status_code=status.HTTP_204_NO_CONTENT
        return resource

    @user_router.get("/all", response_model=FullProfileInfos)
    async def get_list_of_users_paginated(start: int = 0, limit: int = 2):

        users, total = await users_service.get_list_of_users_with_pagenetion(start, limit)
        formatted_users = FullProfileInfos(users = users, total = total)

        return formatted_users

    @user_router.get("/{user_id}", response_model=FullProfileInfo)
    async def get_user_by_id(user_id: int):
        loger.info("Enter function get_user_by_id")
        try:
            full_profile_info = await users_service.get_user_info(user_id)
        except KeyError:
            loger.error(f"User with {user_id} does not existing")
            raise HTTPException(status_code=404, detail={"message":"User does not exists", "user_id":user_id})
        return full_profile_info

    @user_router.patch("/{user_id}", response_model=FullProfileInfo)
    async def update_user(user_id: int, user_profile_info: UserProfileInfo):
        """
        Update some information about user

        :param user_id: int unique Id for updated user
        :param user_profile_info: UserProfileInfo - user's profile information
        :return: FullProfileInfo - full user's profile
        """
        await users_service.update_profile(user_profile_info, user_id)
        full_profile_info = await users_service.get_user_info(user_id)
        return full_profile_info

    @user_router.put("/{user_id}",  response_model=CreateUserResponse)
    async def update_user(user_id: int, full_profile_info: FullProfileInfo):
        user_id = await users_service.create_update_user(full_profile_info, user_id)
        create_user_response = CreateUserResponse(user_id=user_id)
        return create_user_response

    @user_router.delete("/{user_id}")
    async def remove_user(user_id: int):
        try:
            await users_service.delete_user_by_id(user_id)
            return None
        except KeyError:
            raise HTTPException(status_code=404, detail={"message":"User does not exists", "user_id":user_id})

    @user_router.post("/", response_model=CreateUserResponse, status_code=201)
    async def post_user(full_profile_info: FullProfileInfo):
        new_user_id = await users_service.create_user(full_profile_info)
        create_user_response = CreateUserResponse(user_id=new_user_id)
        return create_user_response

    @user_router.on_event("startup")
    async def database_connect():
        await database_client.database.connect()

    @user_router.on_event("shutdown")
    async def database_disconnect():
        await database_client.database.disconnect()

    return user_router
