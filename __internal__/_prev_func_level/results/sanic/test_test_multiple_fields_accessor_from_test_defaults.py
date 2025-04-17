import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    @app.get("/get_with_headers")
    async def get_with_headers(request):
        return text(f"Headers received: {request.headers}")

    request, response = app.test_client.get("/get_with_headers", headers={"Custom-Header": "TestValue"})
    assert response.text == "Headers received: {'custom-header': 'TestValue'}"
    assert response.status == 200

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.get("/get_with_query")
    async def get_with_query(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_query?param=value")
    assert response.text == "Query param: value"
    assert response.status == 200