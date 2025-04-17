import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test")
    async def test_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/test_query")
    async def test_query_handler(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_query?param=value")
    assert response.status == 200
    assert response.text == "Received param: value"

def test_get_method_without_query_param(app):
    @app.get("/test_query_default")
    async def test_query_default_handler(request):
        return text("No param received")

    request, response = app.test_client.get("/test_query_default")
    assert response.status == 200
    assert response.text == "No param received"