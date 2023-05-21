from pydantic import BaseModel, Field
from typing import List, Optional


class User(BaseModel):
    user_name: str = Field(
        title="The user name",
        description="This is user name descrtiption",
        min_length=1,
        max_length=20
    )
    liked_posts: Optional[List[int]] = Field(
        max_items=10
    )


class UserProfileInfo(BaseModel):
    short_description: str
    long_bio: str


class FullProfileInfo(User, UserProfileInfo):
    pass


class FullProfileInfos(BaseModel):
    users: List[FullProfileInfo]
    total: int


class CreateUserResponse(BaseModel):
    user_id: int