import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

def test_get_method(json_app):
    @json_app.get("/get")
    async def handler_get(request: Request):
        return text('I am get method')

    request, response = json_app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(json_app):
    @json_app.get("/get")
    async def handler_get(request: Request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = json_app.test_client.get("/get?param=test")
    assert response.text == 'I am get method with param: test'
    assert response.status == 200

def test_get_method_without_query_param(json_app):
    @json_app.get("/get")
    async def handler_get(request: Request):
        return text('I am get method with param: default')

    request, response = json_app.test_client.get("/get")
    assert response.text == 'I am get method with param: default'
    assert response.status == 200