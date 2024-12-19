import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method_response(app, request_method):
    @app.route('/test_get', methods=[request_method])
    def test_get(request):
        return text('I am get method')

    request, response = app.test_client.get('/test_get') if request_method == 'GET' else app.test_client.post('/test_get')
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.route('/test_get_with_params')
    def test_get_with_params(request):
        param = request.args.get('param', 'default')
        return text(f'Param value is {param}')

    request, response = app.test_client.get('/test_get_with_params?param=test')
    assert response.status == 200
    assert response.text == 'Param value is test'

    request, response = app.test_client.get('/test_get_with_params')
    assert response.status == 200
    assert response.text == 'Param value is default'