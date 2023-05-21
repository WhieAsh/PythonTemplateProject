from app.schemas.users import FullProfileInfo, User, UserProfileInfo
from typing import List, Optional, Tuple
from app.exceptions import UserNotFound, UserAlreadyExists
from app.clients.db import DatabaseClient
from sqlalchemy import select, func, delete, update
from sqlalchemy.sql.expression import Select
from sqlalchemy.dialects.postgresql import insert


class UserService:

    def __init__(self, database_client: DatabaseClient):
        self.database_client = database_client
        self.user_contents = {}
        self.profile_info_contents = {}

    async def get_list_of_users_with_pagenetion(self, offset: int, limit: int) -> Tuple[List[FullProfileInfo], int]:

        list_of_users = []

        users_query = self._get_user_info_query()
        print(users_query)

        users = await self.database_client.get_paginated(users_query, limit, offset)

        for user in users:
            user_info = dict(zip(user.keys(), user.values()))
            full_profile_info = FullProfileInfo(**user_info)
            list_of_users.append(full_profile_info)

        total_query = select(func.count(self.database_client.user.c.id))
        total_res = await self.database_client.get_first(total_query)
        total = total_res[0]

        return list_of_users, total

    async def get_user_info(self, user_id: int = 0) -> FullProfileInfo:

        user_query = self._get_user_info_query(user_id)
        user = await self.database_client.get_first(user_query)

        if not user:
            raise UserNotFound(user_id)

        user_info = dict(zip(user.keys(), user.values()))

        #print(user_info) #this is for test reason

        full_profile_info = FullProfileInfo(**user_info)

        return full_profile_info

    async def create_user(self, full_profile_info: FullProfileInfo) -> int:

        values = dict(username=full_profile_info.user_name,
                       short_description=full_profile_info.short_description,
                       long_bio=full_profile_info.long_bio
        )

        insert_query = (
            insert(self.database_client.user)
            .values(**values)
            .returning(self.database_client.user.c.id)
        )

        insert_query=insert_query.on_conflict_do_nothing(index_elements=["username"])

        res = await self.database_client.get_first(insert_query)

        if not res:
            raise UserAlreadyExists
        new_user_id=res[0]

        return new_user_id

    async def create_update_user(self, full_profile_info: FullProfileInfo, user_id: int) -> int:

        values_no_id = dict(username=full_profile_info.user_name,
                       short_description=full_profile_info.short_description,
                       long_bio=full_profile_info.long_bio
        )

        values = {**values_no_id, "id":user_id}

        user_query = self._get_user_info_query(user_id)
        user = await self.database_client.get_first(user_query)

        if not user:
            query = (
                insert(self.database_client.user)
                .values(**values)
            )
        else:
            query = (
                update(self.database_client.user)
                .values(**values_no_id)
                .where(self.database_client.user.c.id == user_id)
            )

        await self.database_client.execute_in_transaction(query)

        return user_id


    async def update_profile(self, user_profile_info: UserProfileInfo, user_id: int) -> int:

        self.profile_info_contents[user_id] = {
            "short_description": user_profile_info.short_description,
            "long_bio": user_profile_info.long_bio
        }

        return user_id


    async def delete_user_by_id(self, user_id: int):

        delete_query = (
            delete(self.database_client.user)
            .where(self.database_client.user.c.id == user_id)
        )

        await self.database_client.execute_in_transaction(delete_query)
        return None

    def _get_user_info_query(self, user_id: Optional[int] = None) -> Select:

        liked_post_query = (select(
            self.database_client.liked_post.c.user_id,
            func.array_agg(self.database_client.liked_post.c.post_id).label("liked_posts")
            )
            .group_by(self.database_client.liked_post.c.user_id)
        )
        if user_id:
            liked_post_query = liked_post_query.where(self.database_client.liked_post.c.user_id == user_id)

        liked_post_query = liked_post_query.cte("liked_post_query")

        print(liked_post_query)

        user_query = (
            select(self.database_client.user.c.username.label("user_name"),
                   self.database_client.user.c.short_description,
                   self.database_client.user.c.long_bio,
                   self.database_client.user.c.id,
                   liked_post_query.c.liked_posts)
            .join(liked_post_query,
                  liked_post_query.c.user_id == self.database_client.user.c.id,
                  isouter=True)
        )

        if user_id:
            user_query = user_query.where(self.database_client.user.c.id == user_id)

        return user_query
