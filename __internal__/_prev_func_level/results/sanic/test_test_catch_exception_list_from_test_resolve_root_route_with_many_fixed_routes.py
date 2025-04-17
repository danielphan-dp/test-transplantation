import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") == "value"  # Check if header is passed through

def test_get_method_empty_response(app):
    @app.route("/empty")
    def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""