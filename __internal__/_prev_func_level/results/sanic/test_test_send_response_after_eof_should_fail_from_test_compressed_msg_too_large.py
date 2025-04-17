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

def test_send_message_success(app, send, message_stack):
    @app.get("/send")
    async def handler(request: Request):
        await send("Hello, World!")
        return "Message sent"

    _, response = app.test_client.get("/send")
    assert response.text == "Message sent"
    assert message_stack == ["Hello, World!"]

def test_send_multiple_messages(app, send, message_stack):
    @app.get("/send_multiple")
    async def handler(request: Request):
        await send("First message")
        await send("Second message")
        return "Messages sent"

    _, response = app.test_client.get("/send_multiple")
    assert response.text == "Messages sent"
    assert message_stack == ["First message", "Second message"]

def test_send_after_eof_should_fail(app, caplog, message_stack):
    @app.get("/send_after_eof")
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
        _, response = app.test_client.get("/send_after_eof")
        assert "foo, " in response.text
        assert message_in_records(caplog.records, error_msg1)
        assert message_in_records(caplog.records, error_msg2)

def test_send_invalid_type(app, send):
    @app.get("/send_invalid")
    async def handler(request: Request):
        with pytest.raises(TypeError):
            await send({"key": "value"})
        return "Invalid message type"

    _, response = app.test_client.get("/send_invalid")
    assert response.text == "Invalid message type"