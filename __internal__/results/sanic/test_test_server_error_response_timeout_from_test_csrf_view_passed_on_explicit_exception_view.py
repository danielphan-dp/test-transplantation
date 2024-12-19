import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/test_query")
    async def test_query_method(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = app.test_client.get("/test_query?param=test")
    assert response.status == 200
    assert response.text == "Query param is test"

def test_get_method_without_query_param(app):
    request, response = app.test_client.get("/test_query")
    assert response.status == 200
    assert response.text == "Query param is default"