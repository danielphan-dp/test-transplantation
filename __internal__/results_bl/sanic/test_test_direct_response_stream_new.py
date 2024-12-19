import pytest
from sanic import Sanic, Request

@pytest.fixture
def message_stack():
    return []

@pytest.fixture
def send(message_stack):
    async def _send(message):
        message_stack.append(message)
    return _send

@pytest.mark.asyncio
async def test_send_message(send, message_stack):
    await send("test message 1")
    await send("test message 2")
    assert message_stack == ["test message 1", "test message 2"]

@pytest.mark.asyncio
async def test_send_empty_message(send, message_stack):
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_none_message(send, message_stack):
    await send(None)
    assert message_stack == [None]

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    await send("first")
    await send("second")
    await send("third")
    assert message_stack == ["first", "second", "third"]

@pytest.mark.asyncio
async def test_send_large_message(send, message_stack):
    large_message = "a" * 10000
    await send(large_message)
    assert message_stack == [large_message]