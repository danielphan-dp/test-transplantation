import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    def test_get(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/test_get_with_param")
    def test_get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/test_get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_empty_response(app):
    @app.get("/test_get_empty")
    def test_get_empty(request):
        return text("")

    request, response = app.test_client.get("/test_get_empty")
    assert response.status == 200
    assert response.text == ""