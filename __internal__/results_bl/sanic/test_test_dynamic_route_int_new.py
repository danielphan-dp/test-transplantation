import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_empty_response(app):
    @app.route("/get")
    async def get_handler(request):
        return text('')

    request, response = app.test_client.get("/get")
    assert response.text == ''
    assert response.status == 200