import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_method(request: Request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    async def get_with_param(request: Request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "Param is test"

def test_get_method_with_empty_query_param(app):
    @app.get("/get_with_empty_param")
    async def get_with_empty_param(request: Request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get_with_empty_param?param=")
    assert response.text == "Param is "