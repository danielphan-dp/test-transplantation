import pytest
from sanic import Sanic, Request
from sanic.response import json
from logging import ERROR, LogRecord
from typing import Callable, List

@pytest.fixture
def message_in_records():
    def msg_in_log(records: List[LogRecord], msg: str):
        return any(msg in record.message for record in records)
    return msg_in_log

@pytest.mark.asyncio
async def test_send_multiple_messages(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/send_multiple")
    async def send_multiple_handler(request: Request):
        response = await request.respond()
        await response.send("first message")
        await response.send("second message")

    error_msg = "Second respond call is not allowed."

    with caplog.at_level(ERROR):
        _, response = await app.test_client.get("/send_multiple")
        assert response.status == 200
        assert "first message" in response.text
        assert message_in_records(caplog.records, error_msg)

@pytest.mark.asyncio
async def test_send_with_headers(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/send_with_headers")
    async def send_with_headers_handler(request: Request):
        response = await request.respond(headers={"X-Custom-Header": "value"})
        await response.send("message with headers")

    with caplog.at_level(ERROR):
        _, response = await app.test_client.get("/send_with_headers")
        assert response.status == 200
        assert "message with headers" in response.text
        assert "X-Custom-Header" in response.headers
        assert response.headers["X-Custom-Header"] == "value"

@pytest.mark.asyncio
async def test_send_error_on_second_response(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/send_error")
    async def send_error_handler(request: Request):
        response = await request.respond()
        await response.send("first response")
        await response.respond()  # This should trigger an error

    error_msg = "Second respond call is not allowed."

    with caplog.at_level(ERROR):
        _, response = await app.test_client.get("/send_error")
        assert response.status == 500
        assert message_in_records(caplog.records, error_msg)