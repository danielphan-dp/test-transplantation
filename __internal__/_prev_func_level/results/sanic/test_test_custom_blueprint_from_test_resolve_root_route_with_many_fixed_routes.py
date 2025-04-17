import pytest
from sanic import Sanic, Blueprint, text

def test_get_method_response():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_custom_blueprint():
    class Custom(Blueprint):
        def generate_name(self, *objects):
            existing = self._generate_name(*objects)
            return existing.replace("Bar", "CHANGED_BP")

    app = Sanic("test_app", Custom)
    
    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_multiple_requests():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    for _ in range(10):
        request, response = app.test_client.get("/")
        assert response.text == "I am get method"
        assert response.status == 200