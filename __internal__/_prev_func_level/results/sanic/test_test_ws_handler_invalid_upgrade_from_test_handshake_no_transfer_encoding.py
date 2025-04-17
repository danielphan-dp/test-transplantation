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

@pytest.mark.asyncio
async def test_send_message_valid(send, message_stack):
    message = "Hello, WebSocket!"
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_message_empty(send, message_stack):
    message = ""
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_message_binary(send, message_stack):
    message = b"Binary data"
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    messages = ["First message", "Second message"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

@pytest.mark.asyncio
async def test_send_message_invalid_type(send, message_stack):
    with pytest.raises(TypeError):
        await send({"key": "value"})