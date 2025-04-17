import pytest
from connexion import FlaskApp

@pytest.fixture
def app():
    app = FlaskApp(__name__)
    return app

def test_put_method(app):
    @app.put("/v1.0/welcome")
    def put_method(*args, **kwargs):
        kwargs.update({'name': 'put'})
        return (kwargs, 201)

    app_client = app.test_client()

    # Test valid PUT request
    resp = app_client.put("/v1.0/welcome", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json == {'key': 'value', 'name': 'put'}

    # Test PUT request with no data
    resp = app_client.put("/v1.0/welcome")
    assert resp.status_code == 201
    assert resp.json == {'name': 'put'}

    # Test PUT request with unexpected data
    resp = app_client.put("/v1.0/welcome", json={"unexpected": "data"})
    assert resp.status_code == 201
    assert resp.json == {'unexpected': 'data', 'name': 'put'}

    # Test bad operationId
    resp = app_client.put("/v1.0/unknown")
    assert resp.status_code == 501

    # Test invalid method
    resp = app_client.get("/v1.0/welcome")
    assert resp.status_code == 501

    resp = app_client.post("/v1.0/welcome")
    assert resp.status_code == 501

    resp = app_client.delete("/v1.0/welcome")
    assert resp.status_code == 501