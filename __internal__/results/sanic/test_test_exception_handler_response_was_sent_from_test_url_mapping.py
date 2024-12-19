import logging
from typing import Callable, List
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import ServerError

def test_get_method_response(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[logging.LogRecord], str], bool]):
    @app.route("/get")
    async def get_handler(request):
        return text("I am get method")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get")
        assert response.status == 200
        assert response.text == "I am get method"

    message_in_records(
        caplog.records,
        (
            "GET request to /get was successful."
        ),
    )

def test_get_method_invalid_route(app: Sanic):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_logging(app: Sanic, caplog: LogCaptureFixture):
    @app.route("/get_with_logging")
    async def get_with_logging(request):
        return text("Logging test")

    with caplog.at_level(logging.INFO):
        request, response = app.test_client.get("/get_with_logging")
        assert response.status == 200
        assert response.text == "Logging test"
        assert "GET request to /get_with_logging" in caplog.text