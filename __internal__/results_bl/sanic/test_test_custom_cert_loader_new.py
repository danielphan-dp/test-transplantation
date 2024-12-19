import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.testing import SanicTestClient

def test_get_method():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    client = SanicTestClient(app)

    request, response = client.get("/get")
    assert request.scheme == "http"
    assert response.status_code == 200
    assert response.text == 'I am get method'

def test_get_method_not_found():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    client = SanicTestClient(app)

    request, response = client.get("/nonexistent")
    assert response.status_code == 404

def test_get_method_with_query_params():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    client = SanicTestClient(app)

    request, response = client.get("/get?param=value")
    assert request.scheme == "http"
    assert response.status_code == 200
    assert response.text == 'I am get method'