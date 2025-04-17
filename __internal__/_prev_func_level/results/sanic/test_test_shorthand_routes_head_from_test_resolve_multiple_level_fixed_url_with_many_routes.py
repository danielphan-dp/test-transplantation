import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_head_method_empty_response(app):
    @app.head("/head")
    def handler(request):
        return text("OK")

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.body == b''

def test_head_method_not_allowed(app):
    @app.head("/head")
    def handler(request):
        return text("OK")

    request, response = app.test_client.get("/head")
    assert response.status == 405

def test_head_method_with_custom_header(app):
    @app.head("/head")
    def handler(request):
        return text("OK", headers={"Custom-Header": "Value"})

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.headers.get("Custom-Header") == "Value"

def test_head_method_with_no_body(app):
    @app.head("/head")
    def handler(request):
        return text("This should not be returned", headers={'method': 'HEAD'})

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.body == b''

def test_head_method_invalid_route(app):
    request, response = app.test_client.head("/invalid")
    assert response.status == 404