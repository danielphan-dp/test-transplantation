import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def handler(request):
    return text("I am get method")

def test_get_method_response(app):
    bp = Blueprint("Test", version=1.1)
    bp.route("/", version=1.3)(handler)
    app.blueprint(bp, version=1.2)

    request, response = app.test_client.get("/v1.3")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    bp = Blueprint("Test", version=1.1)
    bp.route("/", version=1.3)(handler)
    app.blueprint(bp, version=1.2)

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    bp = Blueprint("Test", version=1.1)
    bp.route("/", version=1.3)(handler)
    app.blueprint(bp, version=1.2)

    request, response = app.test_client.get("/v1.3?param=value")
    assert response.status == 200
    assert response.text == "I am get method"