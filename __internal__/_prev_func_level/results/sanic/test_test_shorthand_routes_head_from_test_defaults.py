import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_head_method(app):
    @app.head("/head")
    def handler(request):
        return text("OK")

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.headers['method'] == 'HEAD'
    
    request, response = app.test_client.get("/head")
    assert response.status == 405

def test_head_empty_response(app):
    @app.head("/empty")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head("/empty")
    assert response.status == 200
    assert response.text == ''
    assert 'Content-Length' in response.headers
    assert response.headers['Content-Length'] == '0'

def test_head_with_custom_header(app):
    @app.head("/custom-header")
    def handler(request):
        return text('', headers={'Custom-Header': 'Value'})

    request, response = app.test_client.head("/custom-header")
    assert response.status == 200
    assert response.headers['Custom-Header'] == 'Value'