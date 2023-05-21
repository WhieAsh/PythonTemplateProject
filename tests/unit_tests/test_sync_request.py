from  requests_test.try_requests import send_sync_get_request
import responses

@responses.activate
def test_syn_get_user_request_work_properly():
    base_url = 'http://127.0.0.1:8000'
    endpoint = '/user/'
    user_id = 0

    responses.add(
        responses.GET,
        f"{base_url}{endpoint}{user_id}",
        json={"user_name" : "test_user"},
        status=200

    )

    response = send_sync_get_request(base_url, endpoint, user_id)

    assert response.json()["user_name"] == "test_user"
    assert type(response.json()) is dict
    assert response.status_code == 200