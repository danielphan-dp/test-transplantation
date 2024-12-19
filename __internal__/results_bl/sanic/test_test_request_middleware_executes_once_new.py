import logging
import asyncio
from itertools import count
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_middleware(app):
    i = count()

    @app.middleware("request")
    async def inc(request):
        nonlocal i
        next(i)

    request, response = app.test_client.get("/get")
    assert next(i) == 1

    request, response = app.test_client.get("/get")
    assert next(i) == 3

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={})
    assert response.status == 200
    assert response.text == 'I am get method'