import pytest
from sanic import Sanic
from sanic.response import text
from sanic_routing.exceptions import RouteExists

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    with pytest.raises(RouteExists):
        @app.route("/get")
        async def another_get_handler(request):
            return text('Another get method')

def test_get_method_with_different_host(app):
    @app.route("/get", host="example.com")
    async def get_handler(request):
        return text('I am get method')

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'I am get method'

def test_get_method_with_no_host(app):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'