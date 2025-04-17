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
    @app.get("/get_with_param")
    async def get_with_param(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == "I am get method with param: test"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/get/invalid")
    assert response.status == 404

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200