import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import PayloadTooLarge

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_payload_too_large_on_get_method(app):
    app.config.REQUEST_MAX_SIZE = 1

    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get", gather_request=False)
    assert response.status == 413
    assert "Request header" in response.text

def test_get_method_with_large_payload(app):
    app.config.REQUEST_MAX_SIZE = 10

    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get", gather_request=False, data='x' * 20)
    assert response.status == 413
    assert "Request header" in response.text

def test_get_method_without_payload(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'