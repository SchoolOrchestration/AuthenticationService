import requests, os, falcon, json
from urllib.parse import parse_qs

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
    '''
    Authenticate the request against an auth backend
    '''
    return {
        "username": username,
        "id": 1
    }

def get_kong_token(client_id, client_secret, user_id):

    base_url = os.environ.get('KONG_BASE_URL')
    provision_key = os.environ.get('KONG_PROVISION_KEY')

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
        "provision_key": provision_key,
        "authenticated_userid": user_id,
    }
    url = "{}/oauth2/token".format(base_url)
    return requests.post(url, data, verify=False)