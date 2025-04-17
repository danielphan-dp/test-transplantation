import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_invalid_route(app):
    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/test?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_multiple_requests(app):
    @app.get("/test")
    async def handler(request):
        return text("I am get method")

    for _ in range(10):
        request, response = app.test_client.get("/test")
        assert response.text == "I am get method"
        assert response.status == 200