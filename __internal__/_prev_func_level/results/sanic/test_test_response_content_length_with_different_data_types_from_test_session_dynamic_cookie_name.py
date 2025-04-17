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

def test_get_method_content_length(app):
    request, response = app.test_client.get("/")
    assert response.headers.get("Content-Length") == "17"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/custom")
    async def custom_get(request):
        return text('Custom header', headers={"X-Custom-Header": "Value"})

    request, response = app.test_client.get("/custom")
    assert response.headers.get("X-Custom-Header") == "Value"