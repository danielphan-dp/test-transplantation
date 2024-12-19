import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    return Sanic("TestApp")

def test_get_method(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_request(app):
    @app.route("/get_empty")
    async def get_empty_handler(request):
        return text('I am get method with empty request')

    request, response = app.test_client.get("/get_empty")
    assert response.status == 200
    assert response.text == 'I am get method with empty request'