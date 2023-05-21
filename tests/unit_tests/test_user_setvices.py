import pytest
from app.exceptions import UserNotFound
from app.schemas.users import FullProfileInfo
from unittest.mock import Mock


@pytest.mark.asyncio
async def test_create_user_work_perfect(user_service, full_profile_info):
    user = await user_service.create_user(full_profile_info)
    assert user is not None
    await user_service.delete_user_by_id(user)

    with pytest.raises(UserNotFound):
        user = await user_service.get_user_info(user)
    return None


@pytest.mark.asyncio
async def test_mocking_create_user_work_perfect(mocking_user_service, mocking_database_client,  full_profile_info):
    user = await mocking_user_service.create_user(full_profile_info)
    mocking_function = Cast(Mock, mocking_database_client.get_first)

    assert mocking_function.called
