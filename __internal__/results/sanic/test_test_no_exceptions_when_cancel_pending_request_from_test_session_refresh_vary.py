import asyncio
import logging
import pytest
from pytest import LogCaptureFixture
from sanic import Sanic
from sanic.response import text

@pytest.mark.xfail(reason="This test runs fine locally, but fails on CI")
def test_get_method_response(app, caplog: LogCaptureFixture, port):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'
    assert "GET /get" in caplog.text

@pytest.mark.xfail(reason="This test runs fine locally, but fails on CI")
def test_get_method_invalid_route(app, caplog: LogCaptureFixture, port):
    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text
    assert "GET /invalid" in caplog.text