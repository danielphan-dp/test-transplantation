import logging
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app, caplog):
    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")
        
        assert response.status == 200
        assert response.text == "I am get method"
        assert ("sanic.access", logging.INFO, "GET /") in caplog.record_tuples

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert response.text == "Requested URL /invalid not found"

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert len(results) == 1
    assert isinstance(results[0], type(response))  # Ensure it's the same type as response

def test_get_method_with_logging(app, caplog):
    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")
        
        assert response.status == 200
        assert "I am get method" in caplog.text

def test_get_method_with_custom_header(app):
    @app.get("/")
    def handler(request):
        return text("I am get method", headers={"X-Custom-Header": "Value"})

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "Value"