import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/test")
def get_method(request):
    return text('I am get method')

def test_get_method(app):
    request, _ = app.test_client.get("/test")
    assert request.status == 200
    assert request.text == 'I am get method'

def test_get_method_not_found(app):
    request, _ = app.test_client.get("/nonexistent")
    assert request.status == 404

def test_get_method_with_context(app):
    @app.route("/context", ctx_foo="foo", ctx_bar=99)
    def context_handler(request):
        return text('Context Test')

    request, _ = app.test_client.get("/context")
    assert request.route.ctx.foo == "foo"
    assert request.route.ctx.bar == 99

def test_get_method_empty_response(app):
    @app.route("/empty")
    def empty_handler(request):
        return text('')

    request, _ = app.test_client.get("/empty")
    assert request.status == 200
    assert request.text == ''