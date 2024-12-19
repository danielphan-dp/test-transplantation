import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_context(app):
    @app.route("/", ctx_foo="foo", ctx_bar=99)
    async def handler_with_context(request):
        return text("I am get method with context")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method with context"
    assert request.route.ctx.foo == "foo"
    assert request.route.ctx.bar == 99

def test_get_method_with_different_http_methods(app):
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text

    request, response = app.test_client.put("/")
    assert response.status == 405
    assert "Method PUT not allowed for URL /" in response.text

    request, response = app.test_client.delete("/")
    assert response.status == 405
    assert "Method DELETE not allowed for URL /" in response.text