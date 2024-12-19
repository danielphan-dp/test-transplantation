import uuid
import unittest.mock
import pytest
from sanic import Sanic
from sanic.response import text, empty
from sanic.exceptions import BadURL, SanicException
from sanic.request import Request
from sanic.server import HttpProtocol

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/test-get")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    @app.get("/invalid")
    async def get(request):
        return text('Invalid route')

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_headers(app):
    @app.get("/test-get-headers")
    async def get(request):
        return text(request.headers.get('Custom-Header', 'No Header'))

    headers = {"Custom-Header": "HeaderValue"}
    request, response = app.test_client.get("/test-get-headers", headers=headers)
    assert response.body == b'HeaderValue'

def test_get_method_protocol(app):
    retrieved = None

    @app.get("/protocol")
    async def get(request):
        nonlocal retrieved
        retrieved = request.protocol
        return empty()

    headers = {"Connection": "keep-alive"}
    _ = app.test_client.get("/protocol", headers=headers)

    assert isinstance(retrieved, HttpProtocol)