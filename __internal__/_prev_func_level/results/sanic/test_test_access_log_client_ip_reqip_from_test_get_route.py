import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_get_method")
    return app

@app.get("/")
async def handler(request):
    return text('I am get method')

def test_get_method_status(app):
    request, response = app.test_client.get("/")
    assert response.status == 200

def test_get_method_response_text(app):
    request, response = app.test_client.get("/")
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/query")
    async def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'not provided')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"

def test_get_method_with_custom_header(app):
    @app.get("/header")
    async def header_handler(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header', 'not provided')}")

    request, response = app.test_client.get("/header", headers={"X-Custom-Header": "test-header"})
    assert response.text == "Header value: test-header"