import pytest
from sanic import Sanic, Blueprint, text

def test_get_method():
    app = Sanic("test_app")
    
    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found():
    app = Sanic("test_app")
    
    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/nonexistent")
    
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param():
    app = Sanic("test_app")
    
    @app.get("/")
    async def get_method(request):
        return text(f"I am get method with param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/?param=test")
    
    assert response.status == 200
    assert response.text == "I am get method with param: test"