import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_with_different_route(app):
    @app.get("/another")
    async def another_handler(request):
        return text("I am another get method")

    request, response = app.test_client.get("/another")
    assert response.status == 200
    assert response.text == "I am another get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/custom")
    async def custom_handler(request):
        return text("I am custom get method", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/custom")
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"