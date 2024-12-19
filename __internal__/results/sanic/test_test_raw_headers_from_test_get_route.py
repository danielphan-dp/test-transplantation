import pytest
from sanic import Sanic
from sanic.text import text

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

def test_get_method_with_custom_headers(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(
        "/",
        headers={
            "Custom-Header": "CustomValue",
            "User-Agent": "TestAgent"
        }
    )

    assert response.status == 200
    assert response.text == "I am get method"
    assert b"Custom-Header: CustomValue" in request.raw_headers
    assert b"User-Agent: TestAgent" in request.raw_headers

def test_get_method_with_invalid_route(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid")

    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.text

def test_get_method_with_empty_response(app):
    @app.get("/")
    async def handler(request):
        return text("")

    request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.text == ""