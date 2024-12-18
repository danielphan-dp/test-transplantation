import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_context(app):
    @app.middleware("request")
    def store(request):
        request.ctx.user = "test_user"
        request.ctx.session = "test_session"

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.ctx.user == "test_user"
    assert request.ctx.session == "test_session"