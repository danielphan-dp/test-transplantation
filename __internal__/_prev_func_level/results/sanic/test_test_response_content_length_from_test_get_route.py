import asyncio
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_content_type(app):
    request, response = app.test_client.get("/get_method")
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_content_length(app):
    request, response = app.test_client.get("/get_method")
    content_length = response.headers.get("Content-Length")
    assert content_length == "17"  # Length of "I am get method"