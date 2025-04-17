import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_content_length(app):
    request, response = app.test_client.get("/get")
    assert response.headers.get("Content-Length") == "17"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/get_with_header")
    async def get_with_header(request):
        return text('I am get method with header', headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/get_with_header")
    assert response.headers.get("X-Custom-Header") == "value"