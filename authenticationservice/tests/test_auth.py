import pytest, falcon, json, responses
from falcon import testing
from authenticationservice.app import api

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
