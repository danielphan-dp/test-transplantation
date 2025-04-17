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

def test_get_method_response(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on query params

def test_get_method_with_headers(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler.get)
    app.blueprint(bp)

    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the handler does not change based on headers