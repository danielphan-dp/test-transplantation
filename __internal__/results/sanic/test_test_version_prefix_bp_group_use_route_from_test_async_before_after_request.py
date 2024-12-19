import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def handler(request):
    return text("I am get method")

def test_get_method(app):
    app.add_route(handler, "/get", methods=["GET"])
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/get_with_param")
    async def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_with_empty_query_param(app):
    @app.get("/get_with_empty_param")
    async def get_with_empty_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_empty_param?param=")
    assert response.status == 200
    assert response.text == "Received param: "