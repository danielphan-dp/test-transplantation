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
    @app.route("/send1")
    async def send_handler1(request: Request):
        response = await request.respond()
        await response.send("first response")
        response = await request.respond()  # This should trigger an error

    @app.route("/send2")
    async def send_handler2(request: Request):
        response = await request.respond()
        await response.send("second response")
        response = await request.respond()  # This should also trigger an error

    error_msg = "Second respond call is not allowed."

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/send1")
        assert response.status == 200
        assert message_in_records(caplog.records, error_msg)

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/send2")
        assert response.status == 500
        assert "500 — Internal Server Error" in response.text

    @app.route("/send3")
    async def send_handler3(request: Request):
        response = await request.respond()
        await response.send("response part 1")
        await response.send("response part 2")  # This should be valid

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/send3")
        assert response.status == 200
        assert "response part 1" in response.text
        assert "response part 2" in response.text
        assert message_in_records(caplog.records, error_msg) is False  # No error should be logged

    @app.route("/send4")
    async def send_handler4(request: Request):
        await request.respond(headers={"test-header": "value"})
        return json({"message": "success"}, headers={"test-header": "another value"})

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/send4")
        assert response.status == 200
        assert response.json["message"] == "success"
        assert "test-header" in response.headers
        assert response.headers["test-header"] == "another value"