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

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_repr(app):
    request, response = app.test_client.get("/")
    assert repr(request) == "<Request: GET />"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_none_method(app):
    request, response = app.test_client.get("/")
    request.method = None
    assert repr(request) == "<Request: None />"

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert request.headers.get("X-Custom-Header") == "value"