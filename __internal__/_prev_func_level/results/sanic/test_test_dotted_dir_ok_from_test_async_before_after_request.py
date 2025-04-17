import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.skipif(sys.platform == 'win32', reason='Windows does not support double dotted directories')
def test_get_method(app: Sanic):
    @app.route('/get')
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get('/get')
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get('/invalid')
    assert response.status == 404
    assert b'Requested URL /invalid not found' in response.body

def test_get_method_with_query_params(app: Sanic):
    @app.route('/get')
    def get_method(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = app.test_client.get('/get?param=test')
    assert response.status == 200
    assert response.body == b'I am get method with param: test'

def test_get_method_without_query_params(app: Sanic):
    @app.route('/get')
    def get_method(request):
        return text('I am get method without params')

    request, response = app.test_client.get('/get')
    assert response.status == 200
    assert response.body == b'I am get method without params'