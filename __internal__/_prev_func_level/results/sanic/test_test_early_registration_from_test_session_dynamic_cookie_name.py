import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test_get")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/test_get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_query")
    async def get_method_with_query(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_get_with_query?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

    request, response = app.test_client.get("/test_get_with_query")
    assert response.text == "Received param: default"
    assert response.status == 200