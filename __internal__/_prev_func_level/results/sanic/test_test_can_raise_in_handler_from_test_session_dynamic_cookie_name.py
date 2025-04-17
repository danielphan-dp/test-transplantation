import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/query")
    async def query_handler(request: Request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_headers(app):
    @app.get("/headers")
    async def headers_handler(request: Request):
        return text(f"Header value: {request.headers.get('X-Custom-Header', 'none')}")

    request, response = app.test_client.get("/headers", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "Header value: value"