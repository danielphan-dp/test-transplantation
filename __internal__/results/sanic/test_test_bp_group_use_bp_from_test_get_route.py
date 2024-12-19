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

def test_get_method_response(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.1?param=test")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on query params

def test_get_method_with_middleware(app, handler):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.1")
    assert response.status == 200
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is request

def test_get_method_response_type(app, handler):
    bp = Blueprint("Test", version=1.1)
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.1")
    assert isinstance(response, text)  # Check if the response is of type text
    assert response.status == 200
    assert response.text == "I am get method"