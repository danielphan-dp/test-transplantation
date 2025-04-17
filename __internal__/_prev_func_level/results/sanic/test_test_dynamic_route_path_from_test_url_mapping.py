import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/test")
    assert response.status == 405

def test_get_method_with_query_params(app):
    @app.get("/test_with_query")
    async def test_with_query(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = app.test_client.get("/test_with_query?param=value")
    assert response.status == 200
    assert response.text == "Query param is value"

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""