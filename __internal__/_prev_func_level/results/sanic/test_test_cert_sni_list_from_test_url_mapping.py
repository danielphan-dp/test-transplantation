import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    async def test_get(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_params")
    async def test_get_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Param is {param}")

    request, response = app.test_client.get("/test_get_with_params?param=test")
    assert response.status == 200
    assert response.text == "Param is test"

def test_get_method_without_query_params(app):
    request, response = app.test_client.get("/test_get_with_params")
    assert response.status == 200
    assert response.text == "Param is default"