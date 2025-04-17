import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    async def get_method_handler(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_method_with_params")
    async def get_method_with_params_handler(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_method_with_params?param=test")
    assert response.status == 200
    assert response.text == "Param is test"

def test_get_method_without_query_params(app):
    request, response = app.test_client.get("/get_method_with_params")
    assert response.status == 200
    assert response.text == "Param is default"