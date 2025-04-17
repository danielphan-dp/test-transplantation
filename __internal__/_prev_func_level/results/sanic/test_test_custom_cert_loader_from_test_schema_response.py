import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    client = SanicTestClient(app)
    request, response = client.get("/get_method")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    client = SanicTestClient(app)
    request, response = client.get("/invalid_route")
    assert response.status_code == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_method_with_params")
    async def get_method_with_params(request):
        return text(f"Received param: {request.args.get('param')}")

    client = SanicTestClient(app)
    request, response = client.get("/get_method_with_params?param=test")
    assert response.status_code == 200
    assert response.text == "Received param: test"

def test_get_method_no_params(app):
    @app.get("/get_method_no_params")
    async def get_method_no_params(request):
        return text("No params received")

    client = SanicTestClient(app)
    request, response = client.get("/get_method_no_params")
    assert response.status_code == 200
    assert response.text == "No params received"