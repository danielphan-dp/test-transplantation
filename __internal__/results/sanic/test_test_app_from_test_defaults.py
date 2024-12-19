import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    app.config.KEEP_ALIVE_TIMEOUT = 1

    @app.get("/")
    async def base_handler(request):
        return text("111122223333444455556666777788889999")

    return app

def test_get_method(app):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/get_with_header")
    async def get_with_header(request):
        return text("I am get method with custom header")

    request, response = app.test_client.get("/get_with_header", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method with custom header"
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    async def get_with_params(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "I am get method with param: test"
    assert response.status == 200

def test_get_method_without_params(app):
    @app.get("/get_without_params")
    async def get_without_params(request):
        return text("I am get method without params")

    request, response = app.test_client.get("/get_without_params")
    assert response.text == "I am get method without params"
    assert response.status == 200