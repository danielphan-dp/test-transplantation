import asyncio
import logging
import pytest
from pytest import LogCaptureFixture
from sanic import Sanic
from sanic.response import text

@pytest.mark.xfail(reason="This test runs fine locally, but fails on CI")
def test_get_method_response(app, caplog: LogCaptureFixture, port):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    client = app.test_client()
    request, response = client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

    with caplog.at_level(logging.INFO):
        request, response = client.get("/get")
    
    assert "Request: GET http:///get" in caplog.text

@pytest.mark.xfail(reason="This test runs fine locally, but fails on CI")
def test_get_method_invalid_route(app, caplog: LogCaptureFixture, port):
    client = app.test_client()
    request, response = client.get("/invalid_route")
    
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

@pytest.mark.xfail(reason="This test runs fine locally, but fails on CI")
def test_get_method_with_logging(app, caplog: LogCaptureFixture, port):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    client = app.test_client()
    with caplog.at_level(logging.INFO):
        request, response = client.get("/get")
    
    assert response.status == 200
    assert "Request: GET http:///get" in caplog.text
    assert response.text == 'I am get method'