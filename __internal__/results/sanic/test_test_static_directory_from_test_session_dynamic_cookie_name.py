import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/get', '/get/'])
def test_get_method(request_path):
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_path', ['/invalid', '/notfound'])
def test_get_method_invalid_path(invalid_path):
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('request_path', ['/get', '/get/'])
def test_get_method_with_query_params(request_path):
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(f"{request_path}?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'