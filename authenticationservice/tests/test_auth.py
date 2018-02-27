import os, pytest, falcon, json, responses
from falcon import testing
from authenticationservice.app import api
from urllib.parse import urlencode

kong_base_url = os.environ.get('KONG_BASE_URL')


@pytest.fixture
def client():
    return testing.TestClient(api)


@responses.activate
def test_login_success(client):

    # verify it makes a request to kong:
    responses.add(
        responses.POST,
        url='{}/users/oauth2/token'.format(kong_base_url),
        json={
            'refresh_token': 'mQpLz8PLSSWFFxEPbaPraWKaC93C3yXc',
            'token_type': 'bearer',
            'access_token': '35gLpRY0akDVFx19x42dtmww2p1btx0v',
            'expires_in': 7200
        },
        status=200
    )
    responses.add(
        responses.POST,
        url='{}/users/login/'.format(kong_base_url),
        json={
            "username": "vumatel_admin",
            "id": 2,
            "organization": "Vumatel",
            "teams": ["vumatel.admin"]
        },
        status=200
    )

    data = {
        'username': 'vumatel_admin',
        'password': '2c3914ea-1779-496d-a6df-c068282b370c',
        'client_id': '9n5tWkjOfFOiiwchAJtXZ7vj7G5Qlw8G',
        'client_secret': 'k2ypqY9emqMilO948I6ZYqNgrFPK5s6i',
    }
    response = client.simulate_post(
                '/auth',
                body=json.dumps(data))

    assert response.status_code == 200


@responses.activate
def test_login_success_form_data(client):

    # verify it makes a request to kong:
    responses.add(
        responses.POST,
        url='{}/users/oauth2/token'.format(kong_base_url),
        json={
            'refresh_token': 'mQpLz8PLSSWFFxEPbaPraWKaC93C3yXc',
            'token_type': 'bearer',
            'access_token': '35gLpRY0akDVFx19x42dtmww2p1btx0v',
            'expires_in': 7200
        },
        status=200
    )
    responses.add(
        responses.POST,
        url='{}/users/login/'.format(kong_base_url),
        json={
            "username": "vumatel_admin",
            "id": 2,
            "organization": "Vumatel",
            "teams": ["vumatel.admin"]
        },
        status=200
    )

    data = urlencode({
        'username': 'joesoap',
        'password': 'testtest',
        'client_id': '1234',
        'client_secret': '5678',
    })
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = client.simulate_post(
                '/auth',
                body=data,
                headers=headers)

    assert response.status_code == 200
