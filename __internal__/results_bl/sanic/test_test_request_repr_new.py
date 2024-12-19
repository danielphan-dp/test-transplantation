import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_repr(app):
    @app.get("/get_repr")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get_repr")
    assert repr(request) == "<Request: GET />"

    request.method = None
    assert repr(request) == "<Request: None />"