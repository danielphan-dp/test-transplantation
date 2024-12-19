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
    bp = Blueprint("Test", version=1.1, version_prefix="/alsoignore/v")
    bp.route("/")(handler)
    app.blueprint(bp, version=1.1, version_prefix="/api/v")

    _, response = app.test_client.get("/api/v/alsoignore/v")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/alsoignore/v")
    bp.route("/")(handler)
    app.blueprint(bp, version=1.1, version_prefix="/api/v")

    _, response = app.test_client.get("/api/v/alsoignore/v/nonexistent")
    assert response.status == 404

def test_get_method_invalid_prefix(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/alsoignore/v")
    bp.route("/")(handler)
    app.blueprint(bp, version=1.1, version_prefix="/api/v")

    _, response = app.test_client.get("/api/v/invalidprefix")
    assert response.status == 404

def test_get_method_with_query_params(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/alsoignore/v")
    bp.route("/")(handler)
    app.blueprint(bp, version=1.1, version_prefix="/api/v")

    _, response = app.test_client.get("/api/v/alsoignore/v?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'