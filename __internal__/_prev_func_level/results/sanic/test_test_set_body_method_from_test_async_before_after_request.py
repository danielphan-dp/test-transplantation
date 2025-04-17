import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

def test_get_method(json_app):
    @json_app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = json_app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found(json_app):
    request, response = json_app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(json_app):
    @json_app.get("/get")
    def get_method_with_param(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = json_app.test_client.get("/get?param=test")
    assert response.text == 'I am get method with param: test'
    assert response.status == 200

def test_get_method_with_empty_query_param(json_app):
    @json_app.get("/get")
    def get_method_with_empty_param(request):
        param = request.args.get('param', 'default')
        return text(f'I am get method with param: {param}')

    request, response = json_app.test_client.get("/get?param=")
    assert response.text == 'I am get method with param: '
    assert response.status == 200