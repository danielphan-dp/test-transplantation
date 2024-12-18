import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_content_length(app):
    request, response = app.test_client.get("/")
    assert response.headers.get("Content-Length") == "17"

def test_get_method_with_query_param(app):
    @app.get("/query")
    async def get_with_query(request: Request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"

def test_get_method_with_empty_query_param(app):
    @app.get("/query")
    async def get_with_query(request: Request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query?param=")
    assert response.text == "Query param: "