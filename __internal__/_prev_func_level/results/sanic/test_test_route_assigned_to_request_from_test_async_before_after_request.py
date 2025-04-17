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
    assert response.status == 200

def test_get_method_route_assigned(app):
    request, _ = app.test_client.get("/get")
    assert request.route is list(app.router.routes)[0]

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get")
    async def get_with_params(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Param is test"
    assert response.status == 200

def test_get_method_without_query_params(app):
    @app.get("/get")
    async def get_with_params(request):
        param = request.args.get('param', 'default')
        return text(f'Param is {param}')

    request, response = app.test_client.get("/get")
    assert response.text == "Param is default"
    assert response.status == 200