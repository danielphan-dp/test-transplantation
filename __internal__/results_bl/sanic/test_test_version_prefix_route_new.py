import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def handler_function(request):
        return text('I am get method')
    return handler_function

def test_get_method_success(app, handler):
    app.route("/get", methods=["GET"])(handler)
    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app, handler):
    app.route("/get", methods=["GET"])(handler)
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_invalid_method(app, handler):
    app.route("/get", methods=["GET"])(handler)
    _, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_empty_route(app, handler):
    app.route("/", methods=["GET"])(handler)
    _, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'