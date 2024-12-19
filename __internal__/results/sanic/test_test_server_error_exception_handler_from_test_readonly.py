import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/test_with_param")
    async def test_get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_without_query_param(app):
    request, response = app.test_client.get("/test_with_param")
    assert response.status == 200
    assert response.text == "Received param: default"