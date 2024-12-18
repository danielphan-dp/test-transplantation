import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/', '/test', '/another_test'])
def test_get_method(request_path):
    app = Sanic("test_app")

    @app.get(request_path)
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_path', ['/invalid', '/not_found'])
def test_get_method_invalid_path(invalid_path):
    app = Sanic("test_app")

    @app.get('/valid')
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_with_query_params(request_path):
    app = Sanic("test_app")

    @app.get(request_path)
    def get_method(request):
        return text('I am get method with query params')

    request, response = app.test_client.get(request_path + '?param=value')
    assert response.status == 200
    assert response.text == 'I am get method with query params'