import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_custom_header(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_different_http_method(app):
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text

def test_get_method_with_query_parameters(app):
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"