import asyncio
import pytest
from sanic import Sanic

@pytest.fixture
def message_stack():
    return []

@pytest.fixture
def send(message_stack):
    async def _send(message):
        message_stack.append(message)
    return _send

@pytest.mark.asyncio
async def test_send_message(send):
    message_stack = []
    await send(b"test message")
    assert message_stack == [b"test message"]

@pytest.mark.asyncio
async def test_send_multiple_messages(send):
    message_stack = []
    await send(b"first message")
    await send(b"second message")
    assert message_stack == [b"first message", b"second message"]

@pytest.mark.asyncio
async def test_send_empty_message(send):
    message_stack = []
    await send(b"")
    assert message_stack == [b""]

@pytest.mark.asyncio
async def test_send_large_message(send):
    message_stack = []
    large_message = b"x" * 10000
    await send(large_message)
    assert message_stack == [large_message]

@pytest.mark.asyncio
async def test_send_non_bytes_message(send):
    message_stack = []
    with pytest.raises(TypeError):
        await send("string message")  # should raise TypeError

@pytest.mark.asyncio
async def test_send_after_closing(send):
    message_stack = []
    await send(b"message before close")
    # Simulate closing the connection
    # Here we would normally have logic to close the connection
    # For this test, we just check the message stack
    assert message_stack == [b"message before close"]