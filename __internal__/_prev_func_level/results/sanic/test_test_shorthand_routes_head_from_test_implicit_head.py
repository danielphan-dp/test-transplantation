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
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.body == b''
    assert response.headers['method'] == 'HEAD'

def test_head_method_with_get(app):
    @app.head("/head")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.get("/head")
    assert response.status == 405

def test_head_method_empty_response(app):
    @app.head("/empty")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head("/empty")
    assert response.status == 200
    assert response.body == b''

def test_head_method_with_custom_header(app):
    @app.head("/custom")
    def handler(request):
        return text('', headers={'X-Custom-Header': 'CustomValue'})

    request, response = app.test_client.head("/custom")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'CustomValue'