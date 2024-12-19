import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def handler(request):
        return text('I am get method')
    return handler

def test_get_method_success(app, handler):
    bp = Blueprint("Test", version=1, version_prefix="/ignore/v")
    bp.route("/get", version=1.1, version_prefix="/api/v")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.1/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app, handler):
    bp = Blueprint("Test", version=1, version_prefix="/ignore/v")
    bp.route("/get", version=1.1, version_prefix="/api/v")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.0/get")
    assert response.status == 404

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test", version=1, version_prefix="/ignore/v")
    bp.route("/get", version=1.1, version_prefix="/api/v")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.1/invalid")
    assert response.status == 404

def test_get_method_no_route(app, handler):
    bp = Blueprint("Test", version=1, version_prefix="/ignore/v")
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.1/get")
    assert response.status == 404