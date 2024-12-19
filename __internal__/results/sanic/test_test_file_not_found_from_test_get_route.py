import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/not_found")
    
    assert response.status == 404
    assert "File not found" in response.text

def test_get_method_with_query_param(app):
    @app.get("/get")
    async def get_handler(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get?param=test")
    
    assert response.status == 200
    assert response.text == "I am get method with param: test"

def test_get_method_with_empty_query_param(app):
    @app.get("/get")
    async def get_handler(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get?param=")
    
    assert response.status == 200
    assert response.text == "I am get method with param: "