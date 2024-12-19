import pytest
from sanic import Sanic, Blueprint
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def get_handler(request):
        return text('I am get method')
    return get_handler

def test_bp_group(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v1")
    assert response.status == 200

def test_get_method_response(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v1")
    assert response.text == 'I am get method'

def test_get_method_not_found(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v2")
    assert response.status == 404

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/invalid_route")
    assert response.status == 404