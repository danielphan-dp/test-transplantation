import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/test")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/test")
    def get_method_with_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/test?param=test_value")
    
    assert response.status == 200
    assert response.text == "I am get method with param: test_value"

def test_get_method_without_query_param(app):
    @app.get("/test")
    def get_method_with_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/test")
    
    assert response.status == 200
    assert response.text == "I am get method with param: default"