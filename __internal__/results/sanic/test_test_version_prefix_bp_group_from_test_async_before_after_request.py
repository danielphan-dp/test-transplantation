import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.fixture
def handler():
    async def handler(request):
        return text("I am get method")
    return handler

def test_get_method_response(app, handler):
    bp = Blueprint("Test")
    bp.route("/get")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app, handler):
    bp = Blueprint("Test")
    bp.route("/get")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming handler does not change based on query params

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text