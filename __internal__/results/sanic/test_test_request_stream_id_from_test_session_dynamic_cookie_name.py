import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_param")
    async def get_with_param(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Param is test"

def test_get_method_without_query_params(app):
    request, response = app.test_client.get("/get_with_param")
    assert response.text == "Param is default"