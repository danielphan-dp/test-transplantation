import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')
    return app

def test_get_method_returns_correct_text(app):
    _, resp = app.test_client.get("/get")
    assert resp.body == b'I am get method'

def test_get_method_status_code(app):
    _, resp = app.test_client.get("/get")
    assert resp.status == 200

def test_get_method_with_invalid_route(app):
    _, resp = app.test_client.get("/invalid")
    assert resp.status == 404

def test_get_method_empty_request(app):
    _, resp = app.test_client.get("/get", data={})
    assert resp.body == b'I am get method'