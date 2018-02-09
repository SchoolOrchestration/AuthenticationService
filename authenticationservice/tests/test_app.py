import falcon
from falcon import testing
import pytest

from authenticationservice.app import api

@pytest.fixture
def client():
    return testing.TestClient(api)


def test_health_endpoint(client):
    response = client.simulate_get('/health')
    assert response.status == falcon.HTTP_OK

def test_get_auth_endpoint(client):
    response = client.simulate_get('/auth')
    assert response.status == falcon.HTTP_OK

def test_post_auth_endpoint(client):
    response = client.simulate_post('/auth')
    assert response.status == falcon.HTTP_OK