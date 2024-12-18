import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_strict_slash(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.get("/get", strict_slashes=False)
    def get_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.get("/get/")
    assert response.text == "OK"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_different_http_method(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text