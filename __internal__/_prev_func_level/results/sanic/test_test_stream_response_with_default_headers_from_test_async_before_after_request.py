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
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.headers["Custom-Header"] != "value"  # Ensure custom header is not returned

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_method(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"