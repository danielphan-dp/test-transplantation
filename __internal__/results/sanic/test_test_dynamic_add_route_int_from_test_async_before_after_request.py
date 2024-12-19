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
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/get")
    async def get_method(request):
        param = request.args.get('param', 'default')
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_with_empty_query_param(app):
    @app.get("/get")
    async def get_method(request):
        param = request.args.get('param', 'default')
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get?param=")
    assert response.text == "Received param: "
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404