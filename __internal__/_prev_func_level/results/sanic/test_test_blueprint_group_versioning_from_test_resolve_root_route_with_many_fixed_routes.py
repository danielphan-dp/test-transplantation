import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f'Query param: {request.args.get("param", "none")}')

    app.add_route(DummyView().get, "/get_with_query")

    request, response = app.test_client.get("/get_with_query?param=test")
    
    assert response.status == 200
    assert response.text == 'Query param: test'

def test_get_method_without_query_params(app):
    class DummyView:
        def get(self, request):
            return text(f'Query param: {request.args.get("param", "none")}')

    app.add_route(DummyView().get, "/get_with_query")

    request, response = app.test_client.get("/get_with_query")
    
    assert response.status == 200
    assert response.text == 'Query param: none'