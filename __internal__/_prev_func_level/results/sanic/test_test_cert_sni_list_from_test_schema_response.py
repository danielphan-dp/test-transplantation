import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    async def get_with_params(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_empty_response(app):
    @app.get("/get_empty")
    async def get_empty(request):
        return text('')

    request, response = app.test_client.get("/get_empty")
    assert response.status == 200
    assert response.text == ""