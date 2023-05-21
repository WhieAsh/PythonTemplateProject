import pytest
from fastapi.testclient import TestClient


def test_user_delete_endpoint_success(test_app, valid_user_id):
    with TestClient(test_app) as test_client:
        response = test_client.delete(f"/user/{valid_user_id}")
        print(response)
        assert response.status_code == 200


# def test_user_get_endpoint_success(test_app, valid_user_id, valid_full_profile_info):
#     with TestClient(test_app) as test_client:
#         response = test_client.get(f"/user/{valid_user_id}")
#         print(response.json())
#         assert response.status_code == 200
#         assert valid_full_profile_info.short_description == response.json()["short_description"]
#         assert valid_full_profile_info.long_bio == response.json()["long_bio"]
#         assert valid_full_profile_info.user_name == response.json()["user_name"]
#         assert valid_full_profile_info.liked_posts == response.json()["liked_posts"]


def test_user_post_endpoint_success(test_app, valid_full_profile_info):
    with TestClient(test_app) as test_client:
        response = test_client.post(url="/user/", json=valid_full_profile_info)
        print(response.json())
        print(response.headers)
        assert response.status_code == 201
        assert response.json()["user_id"] == 1


def test_user_put_endpoint_success(test_app, valid_full_profile_info, valid_user_id):
    with TestClient(test_app) as test_client:
        response = test_client.put(url=f"/user/{valid_user_id}", json=valid_full_profile_info)
        print(response.json())
        print(response.headers)
        assert response.status_code == 200


def test_user_put_user_twice_success(test_app, valid_full_profile_info, valid_user_id):
    with TestClient(test_app) as test_client:
        response = test_client.put(url=f"/user/{valid_user_id}", json=valid_full_profile_info)
        print(response.json())
        print(response.headers)
        assert response.status_code == 200
        response2 = test_client.put(url=f"/user/{valid_user_id}", json=valid_full_profile_info)
        print(response.json())
        print(response.headers)
        assert response.status_code == 200
        assert response.json() == response2.json()


def test_rate_limit(test_app, valid_user_id, valid_full_profile_info):
    with TestClient(test_app) as test_client:
        for i in range(0,20): #This is sending 21 requests when a limit is only 20
            response = test_client.put(url=f"/user/{valid_user_id}", json=valid_full_profile_info)
            if response.status_code == 429:
                assert True
                return
        assert False
