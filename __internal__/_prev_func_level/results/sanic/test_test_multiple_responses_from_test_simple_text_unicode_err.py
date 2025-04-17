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

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_send_multiple_responses(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/test")
    async def test_handler(request: Request):
        response = await request.respond()
        await response.send("first response")
        response = await request.respond()  # This should trigger an error

    error_msg = "Second respond call is not allowed."

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/test")
        assert response.status == 200
        assert "first response" in response.text
        assert message_in_records(caplog.records, error_msg)

def test_send_response_after_finish(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/finish")
    async def finish_handler(request: Request):
        response = await request.respond()
        await response.send("finished")
        await response.send("should not send")  # This should trigger an error

    error_msg = "The response object returned by the route handler will not be sent to client. The request has already been responded to."

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/finish")
        assert response.status == 200
        assert "finished" in response.text
        assert message_in_records(caplog.records, error_msg)

def test_send_with_headers(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/headers")
    async def headers_handler(request: Request):
        response = await request.respond(headers={"X-Custom-Header": "value"})
        await response.send("response with headers")

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/headers")
        assert response.status == 200
        assert "response with headers" in response.text
        assert response.headers["X-Custom-Header"] == "value"

def test_send_empty_response(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool]):
    @app.route("/empty")
    async def empty_handler(request: Request):
        response = await request.respond()
        await response.send("")  # Sending an empty response

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/empty")
        assert response.status == 200
        assert response.text == ""