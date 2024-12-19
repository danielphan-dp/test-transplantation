import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_query")
    async def get_with_query(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.status == 200
    assert response.text == 'Query param is test'

def test_get_method_with_empty_query_params(app):
    @app.get("/get_with_empty_query")
    async def get_with_empty_query(request):
        param = request.args.get('param', 'default')
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/get_with_empty_query")
    assert response.status == 200
    assert response.text == 'Query param is default'