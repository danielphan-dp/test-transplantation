import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    async def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_method")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "TestValue"}
    request, response = app.test_client.get("/get_method", headers=headers)
    
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.headers.get("Custom-Header") == "TestValue"

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_method?param=test")
    
    assert response.status == 200
    assert response.text == "I am get method"