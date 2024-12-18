import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-method")
    async def handler(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get-method")
    assert response.text == 'I am get method'
    assert response.status == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get-method-with-params")
    async def handler(request: Request):
        return text(f'I am get method with param: {request.args.get("param")}')

    request, response = app.test_client.get("/get-method-with-params?param=test")
    assert response.text == 'I am get method with param: test'
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.get("/get-method-with-headers")
    async def handler(request: Request):
        return text('I am get method with headers')

    request, response = app.test_client.get("/get-method-with-headers", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method with headers'
    assert response.status == 200
    assert response.headers["Custom-Header"] == "value"  # This will not be in the response, just testing header handling.