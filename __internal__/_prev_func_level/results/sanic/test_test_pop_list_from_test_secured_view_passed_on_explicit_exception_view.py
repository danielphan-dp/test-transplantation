import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

def test_get_method(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text('I am get method')

    request, response = json_app.test_client.get("/get-method")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid-route")
    assert response.status == 404
    assert b"Requested URL /invalid-route not found" in response.body

def test_get_method_with_query_param(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text(f'I am get method with param: {request.args.get("param", "")}')

    request, response = json_app.test_client.get("/get-method?param=test")
    assert response.text == 'I am get method with param: test'
    assert response.status == 200

def test_get_method_with_empty_query_param(json_app):
    @json_app.get("/get-method")
    async def handler_get(request: Request):
        return text(f'I am get method with param: {request.args.get("param", "")}')

    request, response = json_app.test_client.get("/get-method?param=")
    assert response.text == 'I am get method with param: '
    assert response.status == 200