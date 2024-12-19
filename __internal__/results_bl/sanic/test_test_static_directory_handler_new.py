import os
import pathlib
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.handlers.directory import DirectoryHandler

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get('/get')
    assert response.status == 200
    assert response.content_type == 'text/plain; charset=utf-8'
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get('/nonexistent')
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text(f'I am get method with params: {request.args}')

    _, response = app.test_client.get('/get?param1=value1&param2=value2')
    assert response.status == 200
    assert response.text == 'I am get method with params: OrderedDict([(\'param1\', [\'value1\']), (\'param2\', [\'value2\'])])'