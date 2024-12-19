import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    def get_method(request):
        return text('I am get method')
    return get_method

def test_bp_group_use_bp(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v1.1")
    assert response.status == 200

def test_get_method_response(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/v1.1")
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_no_route(app, handler):
    bp = Blueprint("Test", version=1.1)
    group = Blueprint.group(bp, version=1)
    app.blueprint(group)

    _, response = app.test_client.get("/")
    assert response.status == 404