import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

def test_get_method_response(json_app):
    @json_app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = json_app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route(json_app):
    request, response = json_app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(json_app):
    @json_app.get("/get_with_param")
    def get_with_param(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = json_app.test_client.get("/get_with_param?param=test")
    assert response.text == 'Param is test'
    assert response.status == 200

def test_get_method_with_empty_query_param(json_app):
    @json_app.get("/get_with_empty_param")
    def get_with_empty_param(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = json_app.test_client.get("/get_with_empty_param?param=")
    assert response.text == 'Param is '
    assert response.status == 200

def test_get_method_with_nonexistent_route(json_app):
    request, response = json_app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text