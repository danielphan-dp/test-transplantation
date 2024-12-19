import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def handler(request):
        return text("I am get method")
    return handler

def test_get_method_response(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    app.blueprint(bp, version=1.1)

    request, response = app.test_client.get("/v1.1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    app.blueprint(bp, version=1.1)

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    app.blueprint(bp, version=1.1)

    request, response = app.test_client.get("/v1.1?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming handler does not change based on query params

def test_get_method_with_different_version(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    app.blueprint(bp, version=1.2)

    request, response = app.test_client.get("/v1.2")
    assert response.status == 200
    assert response.text == "I am get method"