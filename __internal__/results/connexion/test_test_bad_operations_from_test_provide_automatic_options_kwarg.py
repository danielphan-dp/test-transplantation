import pytest
from connexion import FlaskApp

@pytest.fixture
def app():
    app = FlaskApp(__name__)
    app.add_url_rule("/v1.0/welcome", view_func=lambda **kwargs: (kwargs, 201), methods=["POST"])
    return app

def test_post_method_with_valid_data(app):
    app_client = app.test_client()
    body = {"key": "value"}
    resp = app_client.post("/v1.0/welcome", json=body)
    assert resp.status_code == 201
    assert resp.json == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(app):
    app_client = app.test_client()
    resp = app_client.post("/v1.0/welcome", json={})
    assert resp.status_code == 201
    assert resp.json == {"name": "post"}

def test_post_method_with_additional_data(app):
    app_client = app.test_client()
    body = {"extra_key": "extra_value"}
    resp = app_client.post("/v1.0/welcome", json=body)
    assert resp.status_code == 201
    assert resp.json == {"extra_key": "extra_value", "name": "post"}

def test_post_method_with_invalid_method(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/welcome")
    assert resp.status_code == 405

def test_post_method_with_unexpected_data(app):
    app_client = app.test_client()
    body = {"unexpected_key": "unexpected_value"}
    resp = app_client.post("/v1.0/welcome", json=body)
    assert resp.status_code == 201
    assert resp.json == {"unexpected_key": "unexpected_value", "name": "post"}