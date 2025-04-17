import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    async def test_get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test_get")
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("content-type") == "text/plain; charset=utf-8"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_additional_params(app):
    @app.get("/test_get_with_params/<param>")
    async def test_get_with_params(request, param):
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_get_with_params/test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_with_empty_response(app):
    @app.get("/test_empty")
    async def test_empty_response(request):
        return text("")

    request, response = app.test_client.get("/test_empty")
    assert response.text == ""
    assert response.status == 200

def test_get_method_with_custom_header(app):
    @app.get("/test_custom_header")
    async def test_custom_header(request):
        return text("Custom header test", headers={"X-Custom-Header": "TestValue"})

    request, response = app.test_client.get("/test_custom_header")
    assert response.headers.get("X-Custom-Header") == "TestValue"