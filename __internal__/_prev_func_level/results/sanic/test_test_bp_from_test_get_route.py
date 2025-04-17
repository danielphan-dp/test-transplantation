import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.fixture
def handler():
    async def handler(request):
        return text("I am get method")
    return handler

def test_get_method(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/v1?param=test")
    assert response.status == 200
    assert response.text == "I am get method"