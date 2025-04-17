import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test-get")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid-route")
    assert response.status == 404
    assert "Requested URL /invalid-route not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/test-get-with-param")
    async def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test-get-with-param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_no_query_param(app):
    request, response = app.test_client.get("/test-get-with-param")
    assert response.status == 200
    assert response.text == "Received param: default"