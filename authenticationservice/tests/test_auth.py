import pytest, falcon, json, responses
from falcon import testing
from authenticationservice.app import api
from urllib.parse import urlencode

@pytest.fixture
def client():
    return testing.TestClient(api)

@responses.activate
def test_login_success(client):

    # verify it makes a request to kong:
    responses.add(
        responses.POST,
        url='http://kong-staging.vumatel.co.za/oauth2/token',
        json={"token_type": "bearer", "access_token": "1234"},
        status=200
    )

    data = {
        'username': 'joesoap',
        'password': 'testtest',
        'client_id': '1234',
        'client_secret': '5678',
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
        url='http://kong-staging.vumatel.co.za/oauth2/token',
        json={"token_type": "bearer", "access_token": "1234"},
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
