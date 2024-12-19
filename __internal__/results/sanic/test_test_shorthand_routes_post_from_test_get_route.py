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

def test_get_route(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_route_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_route_method_not_allowed(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_route_with_query_params(app):
    @app.get("/get_with_param")
    def handler(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"