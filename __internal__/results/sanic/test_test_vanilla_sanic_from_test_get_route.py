import asyncio
from sanic import Sanic, Blueprint, text
from sanic.response import HTTPResponse
import pytest

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.fixture
def test_client(app):
    return app.test_client

class DummyView:
    def get(self, request):
        return text("I am get method")

def test_get_method(app, test_client):
    app.add_route(DummyView().get, "/")
    
    request, response = test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app, test_client):
    request, response = test_client.get("/nonexistent")
    
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app, test_client):
    app.add_route(DummyView().get, "/<param>")
    
    request, response = test_client.get("/test_param")
    
    assert response.status == 200
    assert response.text == "I am get method"  # Adjust based on expected behavior with param

def test_get_method_with_invalid_method(app, test_client):
    app.add_route(DummyView().get, "/")
    
    request, response = test_client.post("/")
    
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text