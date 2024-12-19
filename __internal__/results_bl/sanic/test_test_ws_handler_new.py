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
async def test_send_function_with_valid_message(send, message_stack):
    await send("Hello, World!")
    assert message_stack == ["Hello, World!"]

@pytest.mark.asyncio
async def test_send_function_with_empty_message(send, message_stack):
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_function_multiple_messages(send, message_stack):
    await send("Message 1")
    await send("Message 2")
    await send("Message 3")
    assert message_stack == ["Message 1", "Message 2", "Message 3"]

@pytest.mark.asyncio
async def test_send_function_with_special_characters(send, message_stack):
    await send("!@#$%^&*()")
    assert message_stack == ["!@#$%^&*()"]

@pytest.mark.asyncio
async def test_send_function_with_none(send, message_stack):
    await send(None)
    assert message_stack == [None]