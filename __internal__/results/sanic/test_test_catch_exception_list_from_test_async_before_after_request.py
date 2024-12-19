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

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_method_not_allowed(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_empty_response(app):
    @app.route("/empty")
    def empty_method(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""