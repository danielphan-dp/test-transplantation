import json
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
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "111122223333444455556666777788889999"

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_handler(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/query")
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'not found')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_headers(app):
    @app.get("/headers")
    async def headers_handler(request):
        return text(f"Header: {request.headers.get('X-Custom-Header', 'not found')}")

    request, response = app.test_client.get("/headers", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "Header: value"