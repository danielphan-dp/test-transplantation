import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get('/get')
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.content_type == 'text/plain; charset=utf-8'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get('/invalid')
    assert response.status == 404
    assert response.content_type == 'text/html; charset=utf-8'

def test_get_method_with_custom_header(app):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get('/get', headers={'Custom-Header': 'value'})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.content_type == 'text/plain; charset=utf-8'