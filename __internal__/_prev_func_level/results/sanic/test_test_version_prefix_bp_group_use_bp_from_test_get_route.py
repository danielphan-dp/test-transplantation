import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    class DummyView:
        def get(self, request):
            return text("I am get method")
    return DummyView()

def test_get_method(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/api/v1.1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/api/v1.2")
    assert response.status == 404
    assert "Requested URL /api/v1.2 not found" in response.text

def test_get_method_with_query_param(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/api/v1.1?param=test")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on query params

def test_get_method_with_invalid_method(app, handler):
    bp = Blueprint("Test", version=1.1, version_prefix="/api/v")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.post("/api/v1.1")
    assert response.status == 405
    assert "Method POST not allowed for URL /api/v1.1" in response.text