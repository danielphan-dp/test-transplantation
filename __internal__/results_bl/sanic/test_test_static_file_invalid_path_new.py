import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_valid_request(app):
    @app.get("/test")
    async def test_get(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_request(app):
    @app.get("/test")
    async def test_get(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.parametrize('invalid_path', [{}, [], object()])
def test_get_method_with_invalid_path(app, invalid_path):
    @app.get("/test")
    async def test_get(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404