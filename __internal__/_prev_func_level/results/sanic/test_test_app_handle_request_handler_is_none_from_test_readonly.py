import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    @app.get("/get_with_middleware")
    def handler(request):
        return text("I am get method with middleware")

    request, response = app.test_client.get("/get_with_middleware")
    assert response.text == "I am get method with middleware"
    assert len(results) == 1
    assert results[0] == request

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_without_params(app):
    @app.get("/get_without_params")
    def handler(request):
        return text("No params received")

    request, response = app.test_client.get("/get_without_params")
    assert response.status == 200
    assert response.text == "No params received"