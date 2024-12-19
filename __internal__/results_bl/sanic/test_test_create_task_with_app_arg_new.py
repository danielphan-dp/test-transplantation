import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    @app.route("/get_empty")
    async def get_empty(request):
        return text('I am get method')

    _, response = app.test_client.get("/get_empty", data={})
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    @app.route("/get_query")
    async def get_query(request):
        return text('I am get method with query')

    _, response = app.test_client.get("/get_query?param=test")
    assert response.text == "I am get method with query"

def test_get_method_not_found(app):
    @app.route("/get_not_found")
    async def get_not_found(request):
        return text('Not Found', status=404)

    _, response = app.test_client.get("/get_not_found")
    assert response.status == 404
    assert response.text == "Not Found"