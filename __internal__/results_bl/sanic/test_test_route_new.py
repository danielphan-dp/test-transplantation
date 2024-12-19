import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def handler(request):
        return text('I am get method')
    return handler

def test_route(app, handler):
    app.route("/", version=1)(handler)
    _, response = app.test_client.get("/v1")
    assert response.status == 200

def test_get_method_response(app, handler):
    app.route("/", version=1)(handler)
    _, response = app.test_client.get("/v1")
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app, handler):
    app.route("/", version=1)(handler)
    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_no_version(app, handler):
    app.route("/", version=1)(handler)
    _, response = app.test_client.get("/")
    assert response.status == 404

def test_get_method_with_query_params(app, handler):
    app.route("/", version=1)(handler)
    _, response = app.test_client.get("/v1?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'