import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    async def get(request):
        return text('I am get method')
    return app

def test_get_method(app):
    _, resp = app.test_client.get("/get")
    assert resp.text == "I am get method"

def test_get_method_with_invalid_route(app):
    _, resp = app.test_client.get("/invalid")
    assert resp.status == 404

def test_get_method_with_query_params(app):
    _, resp = app.test_client.get("/get?param=value")
    assert resp.text == "I am get method"

def test_get_method_with_headers(app):
    _, resp = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert resp.text == "I am get method"