import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

def test_get_method():
    app = Sanic("app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    # Test valid GET request
    response = app.test_client.get("/get")
    assert response[1].status == 200
    assert response[0].body == b'I am get method'

    # Test invalid GET request (non-existing route)
    response = app.test_client.get("/non_existing")
    assert response[1].status == 404

    # Test GET request with trailing slash
    response = app.test_client.get("/get/")
    assert response[1].status == 404

    # Test GET request with query parameters
    response = app.test_client.get("/get?param=value")
    assert response[1].status == 200
    assert response[0].body == b'I am get method'