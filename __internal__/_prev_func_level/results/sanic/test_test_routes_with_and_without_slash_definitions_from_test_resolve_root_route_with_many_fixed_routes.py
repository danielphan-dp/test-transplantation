import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    @app.get("/test")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_slash(app):
    @app.get("/test/")
    def get_method_with_slash(request):
        return text('I am get method with slash')

    request, response = app.test_client.get("/test/")
    assert response.status == 200
    assert response.text == 'I am get method with slash'

def test_get_method_with_query_params(app):
    @app.get("/test")
    def get_method_with_query(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'Query param is value'

def test_get_method_without_query_params(app):
    @app.get("/test")
    def get_method_with_query(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'Query param is default'