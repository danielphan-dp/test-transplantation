import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('url', ['/get', '/another_get'])
def test_get_method(app: Sanic, url):
    @app.route(url, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app: Sanic):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.route('/get_with_params', methods=["GET"])
    def get_with_params(request):
        param = request.args.get('param', 'default')
        return text(f'Param value is {param}')

    request, response = app.test_client.get('/get_with_params?param=test')
    assert response.status == 200
    assert response.text == 'Param value is test'

    request, response = app.test_client.get('/get_with_params')
    assert response.status == 200
    assert response.text == 'Param value is default'