import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    @app.get("/get_empty")
    async def get_empty_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get_empty")
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    async def get_with_param_handler(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "I am get method with param: test"