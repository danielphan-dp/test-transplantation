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

def test_get_method_with_custom_header(json_app):
    @json_app.get("/get")
    async def handler_get(request: Request):
        return text('I am get method', headers={'X-Custom-Header': 'value'})

    request, response = json_app.test_client.get("/get")
    assert response.headers['X-Custom-Header'] == 'value'