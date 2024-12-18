import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/test_with_params")
    async def get_with_params(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/test_with_params?param=test")
    assert response.status == 200
    assert response.text == "Param is test"

def test_get_method_without_query_params(app):
    request, response = app.test_client.get("/test_with_params")
    assert response.status == 200
    assert response.text == "Param is default"