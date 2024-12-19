import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def handle_request(request):
        return text('I am get method')
    return handle_request

def test_get_method_success(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.1")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.2")
    assert response.status == 404

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.1/invalid")
    assert response.status == 404

def test_get_method_empty_route(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/api/v1.1/")
    assert response.status == 200
    assert response.text == 'I am get method'