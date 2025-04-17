import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.get("/get")
    async def handler(request):
        return text(f'Query param: {request.args.get("param", "not found")}')

    request, response = app.test_client.get("/get?param=test")
    assert response.text == 'Query param: test'
    assert response.status == 200

def test_get_method_without_query_params(app):
    @app.get("/get")
    async def handler(request):
        return text(f'Query param: {request.args.get("param", "not found")}')

    request, response = app.test_client.get("/get")
    assert response.text == 'Query param: not found'
    assert response.status == 200