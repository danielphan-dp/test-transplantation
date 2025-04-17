import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    def handler(request):
        return text("I am get method")
    return handler

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

    _, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_bp_group_with_query_params(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v1?param=value")
    assert response.status == 200
    assert response.text == "I am get method"