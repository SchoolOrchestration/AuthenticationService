'''
Authentication endpoints
'''
import json, falcon

class AuthenticationResource(object):

    def on_get(self, req, resp):
        resp.body = json.dumps({'todo': True}, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        resp.body = json.dumps({'todo': True}, ensure_ascii=False)
        resp.status = falcon.HTTP_200

#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         data = {
#             "client_id": client_id,
#             "client_secret": client_secret, # testtest
#             "grant_type": "password",
#             "provision_key": settings.KONG_PROVISION_KEY,
#             "authenticated_userid": user.id,
#         }
#         url = "{}/oauth2/token".format(base_url)
#         result = requests.post(url, data, verify=False)
#         status = result.status_code
#         result = result.json()
#     else:
#         result = {
#             'message': 'Authentication failed. Invalid username or password'
#         }
#         status = 401

#     return JsonResponse(result, status=status)
