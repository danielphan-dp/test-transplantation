import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    def handler_function(request):
        return text("I am get method")
    return handler_function

def test_bp_group(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_bp_group_invalid_route(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v2")
    assert response.status == 404
    assert "Requested URL /v2 not found" in response.text

def test_bp_group_method_not_allowed(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.post("/v1")
    assert response.status == 405
    assert "Method POST not allowed for URL /v1" in response.text