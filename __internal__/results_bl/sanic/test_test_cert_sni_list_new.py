import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test_get")
async def test_get_handler(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_params")
    async def handler_with_params(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/test_get_with_params?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_empty_response(app):
    @app.get("/test_empty")
    async def empty_handler(request):
        return text('')

    request, response = app.test_client.get("/test_empty")
    assert response.status == 200
    assert response.text == ''