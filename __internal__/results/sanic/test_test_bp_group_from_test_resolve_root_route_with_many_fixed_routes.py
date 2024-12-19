import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import BadRequest, Forbidden, ServerError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
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
    @app.route("/error")
    def error_route(request):
        raise BadRequest("Invalid")

    request, response = app.test_client.get("/error")
    assert response.status == 400
    assert "Invalid" in response.text

def test_get_method_forbidden(app):
    @app.route("/forbidden")
    def forbidden_route(request):
        raise Forbidden("Forbidden")

    request, response = app.test_client.get("/forbidden")
    assert response.status == 403
    assert "Forbidden" in response.text

def test_get_method_server_error(app):
    @app.route("/server_error")
    def server_error_route(request):
        raise ServerError("Server Error")

    request, response = app.test_client.get("/server_error")
    assert response.status == 500
    assert "Server Error" in response.text