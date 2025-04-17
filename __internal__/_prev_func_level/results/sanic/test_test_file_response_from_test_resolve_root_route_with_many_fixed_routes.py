import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('path', ['/', '/test', '/another_test'])
def test_get_method(app: Sanic, path):
    @app.route(path, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(path)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_path', ['/invalid', '/not_found'])
def test_get_method_invalid_path(app: Sanic, invalid_path):
    @app.route("/valid", methods=["GET"])
    def valid_route(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('method', ['POST', 'PUT', 'DELETE'])
def test_get_method_invalid_http_method(app: Sanic, method):
    @app.route("/", methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.dispatch(method, "/")
    assert response.status == 405
    assert "Method" in response.text