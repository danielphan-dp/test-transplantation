import pytest
from sanic import Sanic
from sanic.response import text
from sanic_routing.exceptions import RouteExists

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    with pytest.raises(RouteExists):
        @app.route("/get")
        async def another_get_method(request):
            return text("Another get method")

def test_get_method_with_custom_host(app):
    @app.route("/get", host="example.com")
    async def custom_host_get(request):
        return text("I am get method on custom host")

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method on custom host"

def test_get_method_with_different_response(app):
    @app.route("/get/alternative")
    async def alternative_get(request):
        return text("Alternative response")

    request, response = app.test_client.get("/get/alternative")
    assert response.text == "Alternative response"