import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_method_not_allowed(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", data=None)
    assert response.status == 200
    assert response.text == 'I am get method'