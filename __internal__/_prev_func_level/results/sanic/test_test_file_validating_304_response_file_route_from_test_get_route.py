import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_with_invalid_route(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get('/invalid')
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_with_custom_header(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    def get_route(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path, headers={'Custom-Header': 'value'})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get('Custom-Header') is None

@pytest.mark.parametrize('request_path', ['/'])
def test_get_method_with_query_params(app: Sanic, request_path: str):
    @app.route(request_path, methods=["GET"])
    def get_route(request):
        return text(f'I am get method with query param: {request.args.get("param")}')

    request, response = app.test_client.get(f"{request_path}?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with query param: test'