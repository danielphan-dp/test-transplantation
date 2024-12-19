import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_allowed(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_param")
    def handler(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"