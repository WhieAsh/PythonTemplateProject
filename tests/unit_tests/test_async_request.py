import pytest
from requests_test.try_requests import send_async_get_request
from aioresponses import aioresponses

@pytest.mark.asyncio
async def test_get_async_request_work_properly():
    base_url = 'http://test.com'
    endpoint = '/user/'
    user_id = 0

    url = base_url + endpoint + str(user_id)

    with aioresponses() as m:
        m.get(
            url,
            payload={"user_name": "test_user"},
            status = 200
        )
        response = await send_async_get_request(base_url, endpoint, user_id)

    json_response = await response.json()

    assert json_response["user_name"] == "test_user"
    assert response.status == 200
