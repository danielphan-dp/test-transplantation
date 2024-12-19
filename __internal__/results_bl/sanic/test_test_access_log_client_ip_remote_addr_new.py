import pytest
from unittest.mock import Mock, ANY
from sanic import Sanic
from sanic.response import text

def test_get_method_response():
    app = Sanic("test_get_method")
    
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route():
    app = Sanic("test_get_method_invalid")

    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_headers():
    app = Sanic("test_get_method_headers")

    @app.route("/get")
    async def get_handler(request):
        return text(request.headers.get('X-Custom-Header', 'No Header'))

    headers = {"X-Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/get", headers=headers)

    assert response.text == 'CustomValue'

def test_get_method_remote_addr():
    app = Sanic("test_get_method_remote_addr")
    access = Mock()

    @app.route("/get")
    async def get_handler(request):
        return text(request.remote_addr)

    headers = {"X-Forwarded-For": "3.3.3.3, 4.4.4.4"}
    request, response = app.test_client.get("/get", headers=headers)

    assert request.remote_addr == "3.3.3.3"