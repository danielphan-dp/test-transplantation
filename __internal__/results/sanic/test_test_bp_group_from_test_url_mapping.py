import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import BadRequest, Forbidden, ServerError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0].path == "/get"

def test_get_method_with_error_handling(app):
    @app.get("/error")
    def error_method(request):
        raise BadRequest("Invalid request")

    request, response = app.test_client.get("/error")
    assert response.status == 400
    assert response.text == "Invalid request"