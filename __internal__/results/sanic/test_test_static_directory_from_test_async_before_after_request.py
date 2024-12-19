import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('uri', ['/get', '/another_get'])
def test_get_method(app, uri):
    @app.get(uri)
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('uri', ['/get', '/another_get'])
def test_get_method_with_query_params(app, uri):
    @app.get(uri)
    def get_method_with_params(request):
        param_value = request.args.get('param', 'default')
        return text(f'I am get method with param: {param_value}')

    request, response = app.test_client.get(f'{uri}?param=test')
    assert response.status == 200
    assert response.text == 'I am get method with param: test'

def test_get_method_not_found(app):
    request, response = app.test_client.get('/non_existent_route')
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_invalid_method(app):
    @app.get('/get')
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.post('/get')
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text