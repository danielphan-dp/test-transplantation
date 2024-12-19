import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, _ = app.test_client.get("/get", headers={"FOO": "bar"})
    assert request.status == 200
    assert request.body == b'I am get method'

def test_get_method_with_custom_headers(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, _ = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert request.status == 200
    assert request.body == b'I am get method'
    assert b'Custom-Header: value' in request.raw_headers

def test_get_method_no_headers(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, _ = app.test_client.get("/get")
    assert request.status == 200
    assert request.body == b'I am get method'
    assert b'Host:' in request.raw_headers
    assert b'User-Agent:' in request.raw_headers

def test_get_method_invalid_route(app):
    @app.route("/invalid", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, _ = app.test_client.get("/nonexistent")
    assert request.status == 404