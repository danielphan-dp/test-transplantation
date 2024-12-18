import asyncio
import pytest
from threading import Event
from sanic.response import text

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.body == b'I am get method'

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

    request, response = app.test_client.post("/get")
    assert response.status == 405

    request, response = app.test_client.put("/get")
    assert response.status == 405

    request, response = app.test_client.delete("/get")
    assert response.status == 405

    request, response = app.test_client.options("/get")
    assert response.status == 200
    assert 'GET' in response.headers['Allow']