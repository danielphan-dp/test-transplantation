import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status_code == 404

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    def handler(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status_code == 200
    assert response.text == "Param is test"

def test_get_method_with_empty_query_param(app):
    @app.get("/get_with_empty_param")
    def handler(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_empty_param?param=")
    assert response.status_code == 200
    assert response.text == "Param is "