import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get")
    async def handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_empty_query_params(app):
    @app.get("/get")
    async def handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get?param=")
    assert response.status == 200
    assert response.text == "Query param: "