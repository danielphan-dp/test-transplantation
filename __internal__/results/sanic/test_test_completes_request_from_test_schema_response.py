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
    @app.get("/")
    async def handler(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"
    assert ("sanic.access", 20, "") in caplog.record_tuples

def test_get_method_with_invalid_route(app, caplog: LogCaptureFixture):
    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text
    assert ("sanic.access", 404, "/invalid") in caplog.record_tuples

def test_get_method_with_logging(app, caplog: LogCaptureFixture):
    @app.get("/")
    async def handler(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"
    
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request >= 0

def test_get_method_with_empty_response(app, caplog: LogCaptureFixture):
    @app.get("/empty")
    async def handler(request):
        return text('')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/empty")
    
    assert response.status == 200
    assert response.text == ""
    assert ("sanic.access", 20, "/empty") in caplog.record_tuples