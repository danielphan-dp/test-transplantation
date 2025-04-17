import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_headers(app):
    request, response = app.test_client.get("/")
    assert "Transfer-Encoding" not in response.headers
    assert "Content-Length" not in response.headers

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.headers["X-Custom-Header"] == "value"