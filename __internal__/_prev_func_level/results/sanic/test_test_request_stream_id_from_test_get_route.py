import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get(request):
        return text('I am get method')

    return app

def test_get_method_status(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_empty_path(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/query")
    async def get_with_query(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param is test"

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/header")
    async def get_with_header(request):
        return text(f'Header value is {request.headers.get("X-Custom-Header", "None")}')

    request, response = app.test_client.get("/header", headers={"X-Custom-Header": "TestValue"})
    assert response.status == 200
    assert response.text == "Header value is TestValue"