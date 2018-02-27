from . import (health, auth)
import falcon

api = application = falcon.API()

api.add_route('/health', health.HealthResource())
api.add_route('/auth', auth.AuthenticationResource())