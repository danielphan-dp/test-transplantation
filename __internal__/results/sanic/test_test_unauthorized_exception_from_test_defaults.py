import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("X-Custom-Header") is None

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""