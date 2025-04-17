import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

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
    bp = Blueprint("Test")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on query params

def test_get_method_with_invalid_method(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text