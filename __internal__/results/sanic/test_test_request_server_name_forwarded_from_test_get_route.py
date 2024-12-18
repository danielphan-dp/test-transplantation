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
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_proxies(app):
    app.config.PROXIES_COUNT = 1
    request, response = app.test_client.get(
        "/",
        headers={
            "Host": "my-server:5555",
            "X-Forwarded-For": "127.1.2.3",
            "X-Forwarded-Host": "your-server",
        },
    )
    assert request.server_name == "your-server"
    assert response.status == 200
    assert response.text == "I am get method"