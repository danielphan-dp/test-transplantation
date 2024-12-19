import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def handler(request):
    return text("I am get method")

def test_bp_get_method(app):
    bp = Blueprint("Test", version=1)
    bp.route("/", version=1.1)(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_bp_get_method_not_found(app):
    bp = Blueprint("Test", version=1)
    bp.route("/", version=1.1)(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.2")
    assert response.status == 404
    assert "Requested URL /v1.2 not found" in response.text

def test_bp_get_method_invalid_method(app):
    bp = Blueprint("Test", version=1)
    bp.route("/", version=1.1)(handler)
    app.blueprint(bp)

    request, response = app.test_client.post("/v1.1")
    assert response.status == 405
    assert "Method POST not allowed for URL /v1.1" in response.text