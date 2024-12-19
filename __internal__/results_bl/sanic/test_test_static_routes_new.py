import asyncio
import re
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/test")
    async def handler1(request):
        return text("OK1")

    @app.route("/pizazz")
    async def handler2(request):
        return text("OK2")

    @app.route("/get")
    async def get_method(request):
        return text("I am get method")

    return app

def test_static_routes(app):
    request, response = app.test_client.get("/test")
    assert response.text == "OK1"

    request, response = app.test_client.get("/pizazz")
    assert response.text == "OK2"

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"