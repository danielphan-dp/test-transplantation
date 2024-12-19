import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/test", methods=["GET"])
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_method_not_allowed(app):
    request, response = app.test_client.post("/test")
    assert response.status == 405

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/test_query", methods=["GET"])
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/test_query?param=value")
    assert response.status == 200
    assert response.text == "Query param: value"