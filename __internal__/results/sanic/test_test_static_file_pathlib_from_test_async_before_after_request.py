import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ['/get', '/another_path'])
def test_get_method(app, request_path):
    @app.get(request_path)
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get('/non_existent_path')
    assert response.status == 404
    assert "Requested URL /non_existent_path not found" in response.text

def test_get_method_with_query_params(app):
    @app.get('/get_with_params')
    def get_with_params(request):
        param_value = request.args.get('param', 'default')
        return text(f'Param value is {param_value}')

    request, response = app.test_client.get('/get_with_params?param=test')
    assert response.status == 200
    assert response.text == 'Param value is test'

    request, response = app.test_client.get('/get_with_params')
    assert response.status == 200
    assert response.text == 'Param value is default'