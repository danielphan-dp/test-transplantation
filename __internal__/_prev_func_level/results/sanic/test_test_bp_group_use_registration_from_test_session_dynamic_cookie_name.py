import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    class Handler:
        def get(self, request):
            return text('I am get method')
    return Handler()

def test_bp_group_use_registration(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group, version=1.2)

    _, response = app.test_client.get("/v1.2")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_bp_group_use_registration_invalid_route(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group, version=1.2)

    _, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_bp_group_use_registration_method_not_allowed(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group, version=1.2)

    _, response = app.test_client.post("/v1.2")
    assert response.status == 405
    assert "Method POST not allowed for URL /v1.2" in response.text