import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/test", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("X-Custom-Header") == "value"  # Check if header is passed

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_handler(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""  # Check for empty response

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/test")
    assert response.status == 405
    assert "Method POST not allowed for URL /test" in response.text