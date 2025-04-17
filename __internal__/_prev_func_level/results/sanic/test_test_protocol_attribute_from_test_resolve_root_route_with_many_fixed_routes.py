import uuid
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.server import HttpProtocol

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_protocol(app):
    retrieved = None

    @app.get("/protocol")
    async def get(request):
        nonlocal retrieved
        retrieved = request.protocol
        return text('Protocol tested')

    headers = {"Connection": "keep-alive"}
    _ = app.test_client.get("/protocol", headers=headers)

    assert isinstance(retrieved, HttpProtocol)

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/custom-header")
    async def get(request):
        return text('Header received', headers={'X-Custom-Header': 'Test'})

    request, response = app.test_client.get("/custom-header")
    
    assert response.headers['X-Custom-Header'] == 'Test'