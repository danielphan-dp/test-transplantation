import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_put_method(app):
    @app.put("/put")
    async def put(request):
        return text("I am put method")

    request, response = app.test_client.put("/put")
    assert response.status == 200
    assert response.text == "I am put method"

def test_put_with_data(app):
    @app.put("/put_with_data")
    async def put_with_data(request):
        return text(request.body.decode("utf-8"))

    data = "Test data"
    request, response = app.test_client.put("/put_with_data", data=data)
    assert response.status == 200
    assert response.text == data

def test_put_empty_body(app):
    @app.put("/put_empty")
    async def put_empty(request):
        return text("Empty body received")

    request, response = app.test_client.put("/put_empty", data="")
    assert response.status == 200
    assert response.text == "Empty body received"

def test_put_invalid_route(app):
    request, response = app.test_client.put("/invalid_route")
    assert response.status == 404

def test_put_with_large_data(app):
    @app.put("/put_large")
    async def put_large(request):
        return text("Received large data")

    large_data = "x" * 10**6  # 1 MB of data
    request, response = app.test_client.put("/put_large", data=large_data)
    assert response.status == 200
    assert response.text == "Received large data"