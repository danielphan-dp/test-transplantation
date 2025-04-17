import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_response(app, request_path):
    @app.route(request_path)
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(app):
    @app.route('/query')
    def get_with_query(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get('/query?param=test')
    assert response.status == 200
    assert response.text == 'Query param is test'