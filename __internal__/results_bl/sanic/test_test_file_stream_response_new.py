import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/test', '/another-test', '/'])
def test_get_method(app: Sanic, request_path):
    @app.route(request_path, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.body == b'I am get method'

@pytest.mark.parametrize('invalid_path', ['/invalid', '/not-found', '/wrong-path'])
def test_get_method_invalid_path(app: Sanic, invalid_path):
    @app.route('/valid', methods=["GET"])
    def valid_route(request):
        return text('I am get method')

    request, response = app.test_client.get(invalid_path)
    assert response.status == 404