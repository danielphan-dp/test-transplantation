import pytest
from sanic import Sanic, Request
from logging import ERROR, LogRecord
from typing import List, Callable

@pytest.fixture
def message_stack():
    return []

@pytest.fixture
def send(message_stack):
    async def _send(message):
        message_stack.append(message)
    return _send

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_send_response_after_eof_should_fail(
    app: Sanic,
    caplog: LogCaptureFixture,
    message_in_records: Callable[[List[LogRecord], str], bool],
    send
):
    @app.get("/")
    async def handler(request: Request):
        response = await request.respond()
        await response.send("foo, ")
        await response.eof()
        await response.send("bar")

    error_msg1 = (
        "The error response will not be sent to the client for the following "
        'exception:"Response stream was ended, no more response '
        'data is allowed to be sent.". A previous '
        "response has at least partially been sent."
    )

    error_msg2 = (
        "Response stream was ended, no more response "
        "data is allowed to be sent."
    )

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/")
        assert "foo, " in response.text
        assert message_in_records(caplog.records, error_msg1)
        assert message_in_records(caplog.records, error_msg2)

def test_send_message_to_stack(send):
    message = "test message"
    await send(message)
    assert message in message_stack

def test_send_multiple_messages_to_stack(send):
    messages = ["message 1", "message 2", "message 3"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

def test_send_empty_message(send):
    await send("")
    assert "" in message_stack

def test_send_none_message(send):
    await send(None)
    assert None in message_stack

def test_send_message_after_eof_should_fail(
    app: Sanic,
    caplog: LogCaptureFixture,
    message_in_records: Callable[[List[LogRecord], str], bool],
    send
):
    @app.get("/eof")
    async def handler(request: Request):
        response = await request.respond()
        await response.eof()
        await send("message after eof")

    error_msg = (
        "Cannot write to websocket interface after it is finished."
    )

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/eof")
        assert message_in_records(caplog.records, error_msg)