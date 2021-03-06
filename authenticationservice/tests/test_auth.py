from authenticationservice.app import api
from urllib.parse import urlencode
from falcon import testing
import responses
import pytest
import redis
import json
import os

kong_base_url = os.environ.get('KONG_BASE_URL')
permissions = os.environ.get('REDIS_PERMISSION_HOST')
redis_permission_host = os.environ.get('REDIS_PERMISSION_HOST')
mock_user_response = {
            'username': 'Natalie',
            'id': 3,
            'organizations': [
                {
                    'name': 'Organization',
                    'id': 3,
                    'groups': [
                        {
                            'name': 'organization.admin',
                            'permissions': [
                                {'name': 'all', 'code': 'code'}
                            ]
                        }
                    ]
                }
            ]
        }


@pytest.fixture
def client():
    return testing.TestClient(api)


@responses.activate
def test_login_success(client):

    # verify it makes a request to kong:
    responses.add(
        responses.POST,
        url='permissions:6379'.format(kong_base_url),
    )
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
        json=mock_user_response,
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
    conn = redis.StrictRedis(redis_permission_host)
    groups_and_permissions = json.loads(conn.get("user_{}".format(3)))
    assert groups_and_permissions['organizations'] is not None


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
        json=mock_user_response,
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
