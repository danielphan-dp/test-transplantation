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
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.data == b''  # HEAD should return no body
    assert response.headers['method'] == 'HEAD'

def test_get_on_head_route(app):
    @app.head("/head")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.get("/head")
    assert response.status == 405  # GET method not allowed

def test_post_on_head_route(app):
    @app.head("/head")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.post("/head")
    assert response.status == 405  # POST method not allowed

def test_options_on_head_route(app):
    @app.head("/head")
    def handler(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.options("/head")
    assert response.status == 405  # OPTIONS method not allowed

def test_head_with_custom_header(app):
    @app.head("/head")
    def handler(request):
        return text('', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'