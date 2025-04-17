import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test/")
    def handler_get(request):
        return text("I am get method")

    return app

def test_get_method_without_slash(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"

def test_get_method_with_slash(app):
    request, response = app.test_client.get("/test/")
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test/?param=value")
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/test/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") is None  # Ensure custom header is not returned in response