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

def test_get_method_status(app):
    request, response = app.test_client.get("/")
    assert response.status == 200

def test_get_method_response_text(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Ensure query params don't affect response text