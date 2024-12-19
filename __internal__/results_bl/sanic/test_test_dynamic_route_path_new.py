import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_dynamic_route(app):
    @app.route("/<path:path>/get")
    async def dynamic_get(request, path):
        return text('Dynamic get method')

    request, response = app.test_client.get("/test/get")
    assert response.status == 200
    assert response.text == 'Dynamic get method'

def test_get_method_with_invalid_path(app):
    request, response = app.test_client.get("/invalid/path")
    assert response.status == 404