import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test_get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_params")
    async def handler(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/test_get_with_params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_with_headers(app):
    @app.get("/test_get_with_headers")
    async def handler(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header')}")

    request, response = app.test_client.get("/test_get_with_headers", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "Header value: value"