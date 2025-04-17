import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get("param", "default")
            return text(f"Received param: {param}")

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/?param=test")
    
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_without_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get("param", "default")
            return text(f"Received param: {param}")

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "Received param: default"