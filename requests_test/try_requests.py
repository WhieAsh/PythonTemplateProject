import requests
import asyncio
import aiohttp


async def send_async_get_request(base_url:str, end_point:str, user_id:int):
    full_url = base_url + end_point + str(user_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(full_url) as async_response:
            json_response = await async_response.json()
            print(json_response["user_name"])
            return async_response


def send_sync_get_request(base_url:str, end_point:str, user_id:int):

    full_url = base_url + end_point + str(user_id)
    response = requests.get(full_url)
    return response


#asyncio.run(send_async_get_request())

#send_sync_get_request('http://127.0.0.1:8000', '/user/', 0)