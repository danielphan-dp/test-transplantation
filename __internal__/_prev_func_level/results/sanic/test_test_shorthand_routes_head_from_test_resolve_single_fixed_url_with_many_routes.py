import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_head_method_response(app):
    @app.head("/head")
    def handler(request):
        return text("OK")

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.headers['method'] == 'HEAD'

def test_head_method_with_get(app):
    @app.head("/head")
    def handler(request):
        return text("OK")

    request, response = app.test_client.get("/head")
    assert response.status == 405

def test_head_method_empty_response(app):
    @app.head("/empty")
    def handler(request):
        return text("")

    request, response = app.test_client.head("/empty")
    assert response.status == 200
    assert response.text == ''

def test_head_method_not_found(app):
    request, response = app.test_client.head("/nonexistent")
    assert response.status == 404

def test_head_method_with_custom_headers(app):
    @app.head("/custom")
    def handler(request):
        return text("OK", headers={"Custom-Header": "Value"})

    request, response = app.test_client.head("/custom")
    assert response.status == 200
    assert response.headers["Custom-Header"] == "Value"