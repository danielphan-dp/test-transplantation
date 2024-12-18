import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)
    
    request, response = app.test_client.get("/test")
    
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0].path == "/test"