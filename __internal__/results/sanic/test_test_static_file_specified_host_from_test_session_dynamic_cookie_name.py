import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('host', ['www.example.com', 'localhost', 'invalid.host'])
def test_get_method_with_host(app, host):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    headers = {"Host": host}
    request, response = app.test_client.get('/get', headers=headers)
    
    if host == 'www.example.com':
        assert response.status == 200
        assert response.text == 'I am get method'
    else:
        assert response.status == 404

@pytest.mark.parametrize('invalid_method', ['POST', 'PUT', 'DELETE'])
def test_get_method_invalid_http_methods(app, invalid_method):
    @app.route('/get', methods=['GET'])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.dispatch(invalid_method, '/get')
    assert response.status == 405
    assert f'Method {invalid_method} not allowed for URL /get' in response.text