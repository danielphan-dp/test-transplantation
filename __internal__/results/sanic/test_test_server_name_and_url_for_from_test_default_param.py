import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_server_name(app):
    app.config.SERVER_NAME = "my-server"
    request, response = app.test_client.get("/test_get")
    assert request.url_for("handler") == "http://my-server/test_get"

def test_get_method_with_https_server_name(app):
    app.config.SERVER_NAME = "https://my-server/path"
    request, response = app.test_client.get("/test_get")
    url = "https://my-server/path/test_get"
    assert request.url_for("handler") == url

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test_get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"