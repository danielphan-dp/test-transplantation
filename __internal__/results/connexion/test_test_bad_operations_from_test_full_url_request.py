import pytest
from connexion import FlaskApp

@pytest.fixture
def app():
    app = FlaskApp(__name__)
    @app.route("/v1.0/welcome", methods=["POST"])
    def welcome_post():
        return post()
    return app

def post(**kwargs):
    kwargs.update({'name': 'post'})
    return (kwargs, 201)

def test_post_success(app):
    app_client = app.test_client()
    resp = app_client.post("/v1.0/welcome", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json[0]['name'] == 'post'
    assert resp.json[0]['key'] == 'value'

def test_post_empty_body(app):
    app_client = app.test_client()
    resp = app_client.post("/v1.0/welcome", json={})
    assert resp.status_code == 201
    assert resp.json[0]['name'] == 'post'

def test_post_with_additional_params(app):
    app_client = app.test_client()
    resp = app_client.post("/v1.0/welcome", json={"extra": "data"})
    assert resp.status_code == 201
    assert resp.json[0]['name'] == 'post'
    assert resp.json[0]['extra'] == 'data'

def test_post_invalid_method(app):
    app_client = app.test_client()
    resp = app_client.get("/v1.0/welcome")
    assert resp.status_code == 501

def test_post_with_query_params(app):
    app_client = app.test_client()
    resp = app_client.post("/v1.0/welcome?query=param", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json[0]['name'] == 'post'
    assert resp.json[0]['key'] == 'value'