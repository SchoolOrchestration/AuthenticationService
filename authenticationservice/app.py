import json, falcon
from . import (health, auth)
api = application = falcon.API()

api.add_route('/health', health.HealthResource())
api.add_route('/auth', auth.AuthenticationResource())