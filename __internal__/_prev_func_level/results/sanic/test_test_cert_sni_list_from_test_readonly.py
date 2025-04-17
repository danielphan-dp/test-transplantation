import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    async def test_get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    @app.get("/test_get_with_param")
    async def test_get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_with_no_query_param(app):
    @app.get("/test_get_with_param")
    async def test_get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_get_with_param")
    assert response.status == 200
    assert response.text == "Received param: default"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(app):
    @app.get("/test_get_with_headers")
    async def test_get_with_headers(request):
        return text(request.headers.get("X-Custom-Header", "No Header"))

    request, response = app.test_client.get("/test_get_with_headers", headers={"X-Custom-Header": "HeaderValue"})
    assert response.status == 200
    assert response.text == "HeaderValue"