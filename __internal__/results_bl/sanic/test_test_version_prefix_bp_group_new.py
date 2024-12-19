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
    bp = Blueprint("Test")
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app, handler):
    bp = Blueprint("Test")
    bp.route("/")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'