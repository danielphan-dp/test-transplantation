import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_strict_slash(app):
    request, response = app.test_client.get("/get/")
    assert response.status == 404

def test_post_method_not_allowed(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404