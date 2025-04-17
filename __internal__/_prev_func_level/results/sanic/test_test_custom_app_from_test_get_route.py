import asyncio
from sanic import Sanic, Blueprint, text
from sanic.response import HTTPResponse

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
    
    @app.get("/valid")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_param():
    app = Sanic("test_app")
    
    @app.get("/")
    async def get_method(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/?param=test")
    
    assert response.status == 200
    assert response.text == "I am get method with param: test"