import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    def handler(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.body

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/test", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.headers.get("X-Custom-Header") is None

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_handler(request: Request):
        return text('')

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.body == b''