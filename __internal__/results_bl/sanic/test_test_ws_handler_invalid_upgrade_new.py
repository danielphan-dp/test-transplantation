import base64
import secrets
import pytest
from sanic import Sanic, Request, Websocket

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

def test_send_message(app, send, message_stack):
    message = "Hello, World!"
    await send(message)
    assert message_stack == [message]

def test_send_multiple_messages(app, send, message_stack):
    messages = ["Hello", "World", "!"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

def test_send_empty_message(app, send, message_stack):
    message = ""
    await send(message)
    assert message_stack == [message]

def test_send_none_message(app, send, message_stack):
    message = None
    await send(message)
    assert message_stack == [message]