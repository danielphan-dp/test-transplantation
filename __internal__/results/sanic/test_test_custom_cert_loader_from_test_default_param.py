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

def test_get_method_with_query_param(app):
    @app.get("/get_method_with_param")
    async def get_method_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    client = SanicTestClient(app)
    request, response = client.get("/get_method_with_param?param=test")
    assert response.status_code == 200
    assert response.text == "Received param: test"

def test_get_method_no_query_param(app):
    @app.get("/get_method_with_param")
    async def get_method_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    client = SanicTestClient(app)
    request, response = client.get("/get_method_with_param")
    assert response.status_code == 200
    assert response.text == "Received param: default"