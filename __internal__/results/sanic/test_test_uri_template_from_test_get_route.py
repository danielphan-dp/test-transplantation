import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure query params don't affect response

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/test", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure headers don't affect response

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""  # Test for empty response body