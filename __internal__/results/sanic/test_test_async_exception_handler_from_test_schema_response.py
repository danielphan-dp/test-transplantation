import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    async def test_get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_params")
    async def test_get_with_params(request):
        name = request.args.get('name', 'World')
        return text(f"Hello, {name}")

    request, response = app.test_client.get("/test_get_with_params?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice"

def test_get_method_no_query_params(app):
    request, response = app.test_client.get("/test_get_with_params")
    assert response.status == 200
    assert response.text == "Hello, World"