import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test-get")
    async def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/test-get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.get("/test-get-with-params")
    async def get_with_params(request: Request):
        name = request.args.get("name", "default")
        return text(f"I am get method with name: {name}")

    request, response = app.test_client.get("/test-get-with-params?name=John")
    assert response.text == "I am get method with name: John"
    assert response.status == 200

def test_get_method_with_no_query_params(app):
    @app.get("/test-get-with-no-params")
    async def get_with_no_params(request: Request):
        return text("I am get method with no params")

    request, response = app.test_client.get("/test-get-with-no-params")
    assert response.text == "I am get method with no params"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    request, response = app.test_client.get("/test-get")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert type(results[0]) is Request