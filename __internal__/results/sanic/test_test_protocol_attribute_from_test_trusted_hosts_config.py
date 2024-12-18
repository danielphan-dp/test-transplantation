import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_protocol(app):
    retrieved = None

    @app.get("/")
    async def get(request):
        nonlocal retrieved
        retrieved = request.protocol
        return text('I am get method')

    headers = {"Connection": "keep-alive"}
    _ = app.test_client.get("/", headers=headers)

    assert isinstance(retrieved, str)  # Assuming protocol is a string type