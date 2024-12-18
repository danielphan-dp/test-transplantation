import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b'I am get method'

def test_get_method_empty_query(app):
    request, response = app.test_client.get("/get?query=")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.body == b'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.body

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_with_different_content_type(app):
    request, response = app.test_client.get("/get", headers={"Accept": "application/json"})
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"  # Content type should remain unchanged
    assert response.body == b'I am get method'