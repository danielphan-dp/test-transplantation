import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.fixture
def handler():
    async def handler(request):
        return text("I am get method")
    return handler

def test_get_method(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/", version=1.1)(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/", version=1.1)(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/", version=1.1)(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1.1?param=value")
    assert response.status == 200
    assert response.text == "I am get method"