import os
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

    _, response = app.test_client.get('/get')
    assert response.status == 200
    assert response.body == b'I am get method'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'

def test_get_method_invalid_route(app):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get('/invalid_route')
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get('/get?param=value')
    assert response.status == 200
    assert response.body == b'I am get method'