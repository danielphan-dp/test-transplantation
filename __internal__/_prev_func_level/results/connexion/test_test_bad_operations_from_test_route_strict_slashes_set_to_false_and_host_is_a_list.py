import pytest
from connexion import FlaskApp

@pytest.fixture
def app():
    app = FlaskApp(__name__)
    return app

def test_put_method_with_valid_data(app):
    app_client = app.test_client()
    
    resp = app_client.put("/v1.0/welcome", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json == {'key': 'value', 'name': 'put'}

def test_put_method_with_empty_data(app):
    app_client = app.test_client()
    
    resp = app_client.put("/v1.0/welcome", json={})
    assert resp.status_code == 201
    assert resp.json == {'name': 'put'}

def test_put_method_with_invalid_endpoint(app):
    app_client = app.test_client()
    
    resp = app_client.put("/v1.0/nonexistent")
    assert resp.status_code == 501

def test_put_method_with_additional_parameters(app):
    app_client = app.test_client()
    
    resp = app_client.put("/v1.0/welcome", json={"extra": "data"})
    assert resp.status_code == 201
    assert resp.json == {'extra': 'data', 'name': 'put'}