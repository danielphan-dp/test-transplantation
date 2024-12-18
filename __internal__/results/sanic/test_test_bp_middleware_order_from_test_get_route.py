import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is request

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_response(app):
    class DummyView:
        def get(self, request):
            return text("Custom response", status=201)

    app.add_route(DummyView().get, "/")

    request, response = app.test_client.get("/")

    assert response.status == 201
    assert response.text == "Custom response"