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
    assert response.body == b"I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert b"Requested URL /nonexistent not found" in response.body

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.body == b"I am get method"  # Ensure query params do not affect response

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.body == b"I am get method"  # Ensure headers do not affect response