'''
Authentication endpoints
'''
import json, falcon, os
from . import BaseResource, validate
from .schemas import load_schema
from .helpers import authenticate, get_kong_token, status_string

class AuthenticationResource(object):

    def on_get(self, req, resp):
        resp.body = json.dumps({'todo': True}, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    @validate(load_schema('login'))
    def on_post(self, req, resp, parsed):
        username = parsed.get('username')
        password = parsed.get('password')
        client_id = parsed.get('client_id')
        client_secret = parsed.get('client_secret')

        user = authenticate(username=username, password=password)

        if user is not None:
            result = get_kong_token(client_id, client_secret, user.get('id'))
            resp.body = json.dumps(result.json(), ensure_ascii=False)
            resp.status = status_string(result.status_code)
        else:
            result = {
                'message': 'Authentication failed. Invalid username or password'
            }
            resp.body = json.dumps(json.dumps(result), ensure_ascii=False)
            resp.status = falcon.HTTP_403
