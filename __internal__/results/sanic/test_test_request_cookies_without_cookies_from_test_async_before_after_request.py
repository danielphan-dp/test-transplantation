import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_cookies(app):
    request, response = app.test_client.get("/get", cookies={"session_id": "12345"})
    assert request.cookies == {"session_id": "12345"}
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_without_cookies(app):
    request, response = app.test_client.get("/get")
    assert request.cookies == {}
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/get", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers["X-Custom-Header"] == "value"