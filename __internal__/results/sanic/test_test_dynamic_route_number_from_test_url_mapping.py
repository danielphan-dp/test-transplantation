import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/query")
    async def get_with_query(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_with_empty_query_params(app):
    @app.get("/query")
    async def get_with_query(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query")
    assert response.text == "Query param: none"
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.get("/headers")
    async def get_with_headers(request):
        return text(f"Header: {request.headers.get('X-Custom-Header', 'none')}")

    request, response = app.test_client.get("/headers", headers={"X-Custom-Header": "value"})
    assert response.text == "Header: value"
    assert response.status == 200

def test_get_method_with_invalid_method(app):
    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text