import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_method_not_allowed(app):
    @app.get("/method")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.post("/method")
    assert response.status == 405
    assert "Method POST not allowed for URL /method" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/custom")
    async def get_method(request):
        return text("I am get method", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/custom")
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"