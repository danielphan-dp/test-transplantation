import logging
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/non_existing_route")
    
    assert response.status == 404
    assert response.text == "Not Found"

def test_get_method_logging(app, caplog):
    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")

    assert response.status == 200
    assert "I am get method" in caplog.text
    assert caplog.record_tuples == []  # No errors should be logged

def test_get_method_with_query_param(app):
    @app.get("/get")
    async def get_handler(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = app.test_client.get("/get?param=test")
    
    assert response.status == 200
    assert response.text == "I am get method with param: test"