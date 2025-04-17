import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_response_headers(app):
    request, response = app.test_client.get("/")
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert "content-length" in response.headers

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"  # This will not be present, just testing behavior

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_method(request: Request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200