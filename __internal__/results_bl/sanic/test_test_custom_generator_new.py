import uuid
import unittest.mock.Mock
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

def test_get_method():
    app = Sanic("test_get_method")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_request():
    app = Sanic("test_get_method_invalid")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"Invalid-Header": "value"})
    assert response.text == 'I am get method'  # Ensure it still responds correctly

def test_get_method_with_empty_request():
    app = Sanic("test_get_method_empty")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={})
    assert response.text == 'I am get method'  # Ensure it still responds correctly

def test_get_method_with_custom_request_id():
    REQUEST_ID = 99

    class CustomRequest(Request):
        @classmethod
        def generate_id(cls, request):
            return int(request.headers.get("some-other-request-id", 0)) * 2

    app = Sanic("test_get_method_custom_request", request_class=CustomRequest)

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/get", headers={"some-other-request-id": f"{REQUEST_ID}"}
    )
    assert request.id == REQUEST_ID * 2
    assert response.text == 'I am get method'  # Ensure it still responds correctly