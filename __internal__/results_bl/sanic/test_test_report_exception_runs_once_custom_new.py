import asyncio
import pytest
from sanic import Sanic, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_returns_text(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_handler(request):
        return text(f'I am get method with param: {request.args.get("param")}')

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with param: test'