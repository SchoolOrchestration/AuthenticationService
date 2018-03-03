from urllib.parse import parse_qs
import requests
import falcon
import redis
import json
import os

KONG_BASE_URL = os.environ.get('KONG_BASE_URL')
REDIS_PERMISSION_HOST = os.environ.get('REDIS_PERMISSION_HOST')
PROVISION_KEY = os.environ.get('KONG_PROVISION_KEY')


def status_string(status_code):
    return getattr(falcon, 'HTTP_{}'.format(status_code))


def get_data(req):
    content_type = req.get_header('content_type')
    body = req.stream.read()
    if content_type == 'application/x-www-form-urlencoded':
        return parse_qs(body)
    else:
        return json.loads(body.decode('utf-8'))


def authenticate(username, password):
    """
    Authenticate the request against an auth backend
    """
    response = requests.post(
        "{}/users/login/".format(KONG_BASE_URL),
        {
            'username': username,
            'password': password
        }
    )
    if response.status_code == 200:
        return response.json()
    return None


def get_kong_token(client_id, client_secret, user_id):
    """
    Gets a authentication token set from kong to pass back to client
    """
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
        "provision_key": PROVISION_KEY,
        "authenticated_userid": user_id,
    }
    url = "{}/users/oauth2/token".format(KONG_BASE_URL)
    return requests.post(url, data, verify=False)


def push_groups_to_redis(user_id, data):
    """
    Pushes a dict of user groups and permissions to a redis host
    """
    conn = redis.StrictRedis(REDIS_PERMISSION_HOST)
    p_data = json.dumps(data)
    conn.set("authorization.{}".format(user_id), p_data)
