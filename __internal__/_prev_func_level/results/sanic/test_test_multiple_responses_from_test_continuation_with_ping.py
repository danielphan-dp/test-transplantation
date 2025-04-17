import pytest
from sanic import Sanic, Request
from sanic.response import json
from logging import ERROR, LogRecord
from typing import List, Callable

@pytest.fixture
def message_in_records():
    def msg_in_log(records: List[LogRecord], msg: str):
        return any(msg in record.message for record in records)
    return msg_in_log

@pytest.mark.asyncio
async def test_send_multiple_responses(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/test")
    async def test_handler(request: Request):
        response = await request.respond()
        await response.send("first response")
        response = await request.respond()  # This should trigger an error

    error_msg = "Second respond call is not allowed."

    with caplog.at_level(ERROR):
        _, response = await app.test_client.get("/test")
        assert response.status == 200
        assert message_in_records(caplog.records, error_msg)

@pytest.mark.asyncio
async def test_send_with_headers(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/test_headers")
    async def test_headers_handler(request: Request):
        response = await request.respond(headers={"X-Custom-Header": "value"})
        await response.send("response with headers")
        return json({"status": "done"}, headers={"X-Custom-Header": "value"})

    with caplog.at_level(ERROR):
        _, response = await app.test_client.get("/test_headers")
        assert response.status == 200
        assert "response with headers" in response.text
        assert "X-Custom-Header" in response.headers
        assert response.headers["X-Custom-Header"] == "value"

@pytest.mark.asyncio
async def test_send_empty_response(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/test_empty")
    async def test_empty_handler(request: Request):
        response = await request.respond()
        await response.send("")  # Sending an empty response
        return json({"status": "empty"})

    with caplog.at_level(ERROR):
        _, response = await app.test_client.get("/test_empty")
        assert response.status == 200
        assert response.text == '{"status":"empty"}'

@pytest.mark.asyncio
async def test_send_multiple_empty_responses(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/test_multiple_empty")
    async def test_multiple_empty_handler(request: Request):
        response = await request.respond()
        await response.send("")  # First empty response
        response = await request.respond()  # This should trigger an error

    error_msg = "Second respond call is not allowed."

    with caplog.at_level(ERROR):
        _, response = await app.test_client.get("/test_multiple_empty")
        assert response.status == 200
        assert message_in_records(caplog.records, error_msg)