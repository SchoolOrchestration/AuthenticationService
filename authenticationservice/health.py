"""
Health endpoint
"""
import json, falcon


def check_kong_is_ok():
    """TBD"""
    return 'TBD'


class HealthResource(object):

    @staticmethod
    def on_get(req, resp):
        doc = {
            "status": {
                "status": "OK",
                "kong": check_kong_is_ok(),
                "version": "1"
            }
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
