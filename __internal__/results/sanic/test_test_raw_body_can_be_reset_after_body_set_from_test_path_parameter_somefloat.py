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
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    @app.get("/test_with_param")
    async def test_get_with_param(request):
        param = request.args.get('param', 'default')
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_with_param?param=test")
    assert response.text == "Received param: test"

def test_get_method_with_no_query_param(app):
    @app.get("/test_with_param")
    async def test_get_with_param(request):
        param = request.args.get('param', 'default')
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_with_param")
    assert response.text == "Received param: default"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/test_with_header")
    async def test_get_with_header(request):
        return text("Header received", headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/test_with_header")
    assert response.headers["X-Custom-Header"] == "value"