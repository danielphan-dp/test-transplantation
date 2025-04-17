import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_with_different_path(app):
    @app.get("/another")
    async def handler(request):
        return text("I am get method at another path")

    request, response = app.test_client.get("/another")
    assert response.status == 200
    assert response.text == "I am get method at another path"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_with_invalid_path(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_headers(app):
    @app.get("/custom")
    async def handler(request):
        return text("I am get method with custom headers", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/custom")
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"