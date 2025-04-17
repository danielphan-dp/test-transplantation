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

def test_get_method(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test_with_params")
    async def test_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Param is {param}")

    request, response = app.test_client.get("/test_with_params?param=value")
    assert response.status == 200
    assert response.text == "Param is value"

def test_get_method_with_empty_query_params(app):
    request, response = app.test_client.get("/test_with_params")
    assert response.status == 200
    assert response.text == "Param is default"