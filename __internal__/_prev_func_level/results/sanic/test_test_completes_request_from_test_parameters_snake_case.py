import asyncio
import logging
import pytest
from pytest import LogCaptureFixture
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app, caplog: LogCaptureFixture):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")

    assert response.status_code == 200
    assert response.text == 'I am get method'
    assert ("sanic.access", 20, "/get") in caplog.record_tuples

def test_get_method_with_logging(app, caplog: LogCaptureFixture):
    @app.get("/get-logged")
    async def handler(request):
        return text('I am get method with logging')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get-logged")

    assert response.status_code == 200
    assert response.text == 'I am get method with logging'
    assert ("sanic.access", 20, "/get-logged") in caplog.record_tuples

def test_get_method_empty_response(app):
    @app.get("/get-empty")
    async def handler(request):
        return text('')

    request, response = app.test_client.get("/get-empty")
    assert response.status_code == 200
    assert response.text == ''

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non-existent")
    assert response.status_code == 404
    assert "Requested URL /non-existent not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get-query")
    async def handler(request):
        name = request.args.get('name', 'Guest')
        return text(f'Hello, {name}!')

    request, response = app.test_client.get("/get-query?name=John")
    assert response.status_code == 200
    assert response.text == 'Hello, John!'