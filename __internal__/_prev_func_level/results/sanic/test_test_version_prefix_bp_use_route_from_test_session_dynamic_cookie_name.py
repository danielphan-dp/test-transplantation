import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def handler(request):
    return text("I am get method")

def test_get_method_response(app):
    bp = Blueprint("Test", version=1, version_prefix="/api/v")
    bp.route("/get", version=1.1, version_prefix="/api/v")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/api/v1.1/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    bp = Blueprint("Test", version=1, version_prefix="/api/v")
    bp.route("/get", version=1.1, version_prefix="/api/v")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/api/v1.2/get")
    assert response.status == 404
    assert "Requested URL /api/v1.2/get not found" in response.text

def test_get_method_with_different_prefix(app):
    bp = Blueprint("Test", version=1, version_prefix="/api/v")
    bp.route("/get", version=1.1, version_prefix="/api/v")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/api/v/get")
    assert response.status == 200
    assert response.text == "I am get method"