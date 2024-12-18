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

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_server_name(app):
    app.config.SERVER_NAME = "my-server"
    request, response = app.test_client.get("/get")
    assert request.url_for("get_method") == "http://my-server/get"

def test_get_method_with_https_server_name(app):
    app.config.SERVER_NAME = "https://my-server/path"
    request, response = app.test_client.get("/get")
    assert request.url_for("get_method") == "https://my-server/path/get"