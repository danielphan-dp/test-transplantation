import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_large_payload(app):
    app.config.REQUEST_MAX_SIZE = 1  # Set max size to 1 byte
    request, response = app.test_client.get("/get", data="x" * 10)  # Sending large payload
    assert response.status == 413
    assert "Request header" in response.text

def test_get_method_no_payload(app):
    request, response = app.test_client.get("/get", data="")
    assert response.status == 200
    assert response.text == "I am get method"