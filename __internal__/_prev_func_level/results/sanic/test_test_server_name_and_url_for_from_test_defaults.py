import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_url(app):
    app.config.SERVER_NAME = "my-server"
    request, response = app.test_client.get("/get_method")
    assert request.url_for("get_method") == "http://my-server/get_method"

    app.config.SERVER_NAME = "https://my-server/path"
    request, response = app.test_client.get("/get_method")
    assert request.url_for("get_method") == "https://my-server/path/get_method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_method?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure query params do not affect response

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get_method", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure headers do not affect response