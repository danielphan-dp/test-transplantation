import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test")
    async def test_get(request):
        return text('I am get method')

    _, response = app.test_client.get("/test")
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_route(app):
    @app.get("/")
    async def empty_route(request):
        return text('Root route')

    _, response = app.test_client.get("/")
    assert response.text == 'Root route'