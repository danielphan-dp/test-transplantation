import uuid
import unittest.mock.Mock
from uuid import UUID, uuid4
import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("test_get_method")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    request, _ = app.test_client.get("/get")
    assert request.status == 200
    assert request.text == 'I am get method'

    request, _ = app.test_client.get("/get", headers={"Accept": "text/plain"})
    assert request.status == 200
    assert request.text == 'I am get method'

    request, _ = app.test_client.get("/get", headers={"Accept": "application/json"})
    assert request.status == 200
    assert request.text == 'I am get method'

    request, _ = app.test_client.get("/get", headers={"Accept": "text/html"})
    assert request.status == 200
    assert request.text == 'I am get method'

    request, _ = app.test_client.get("/get", headers={"Accept": "invalid/type"})
    assert request.status == 200
    assert request.text == 'I am get method'