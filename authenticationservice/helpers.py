import requests, os, falcon, json
from urllib.parse import parse_qs
import pickle
import redis
import json

KONG_BASE_URL = os.environ.get('KONG_BASE_URL')
REDIS_PERMISSION_HOST = os.environ.get('REDIS_PERMISSION_HOST')


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

    base_url = KONG_BASE_URL
    provision_key = os.environ.get('KONG_PROVISION_KEY')
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
        "provision_key": provision_key,
        "authenticated_userid": user_id,
    }
    url = "{}/users/oauth2/token".format(base_url)
    return requests.post(url, data, verify=False)


def push_groups_to_redis(user_id, groups, permissions=None):
    """
    Pushes a dict of user groups and permissions to a redis host
    """
    conn = redis.StrictRedis(REDIS_PERMISSION_HOST)
    data = {
        'groups': groups,
        'permissions': permissions
    }
    p_data = pickle.dumps(data)
    conn.set(user_id, p_data)
