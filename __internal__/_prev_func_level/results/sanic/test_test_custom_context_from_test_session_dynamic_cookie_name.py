import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_context(app):
    @app.middleware("request")
    def store(request):
        request.ctx.user = "test_user"
        request.ctx.session = None

    @app.route("/get_with_context")
    def get_with_context(request):
        return text(f"User: {request.ctx.user}, Session: {request.ctx.session}")

    request, response = app.test_client.get("/get_with_context")
    assert response.text == "User: test_user, Session: None"