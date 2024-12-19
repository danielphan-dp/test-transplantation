import pytest
from unittest.mock import Mock

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
    await send("Hello, World!")
    assert message_stack == ["Hello, World!"]

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    await send("Message 1")
    await send("Message 2")
    assert message_stack == ["Message 1", "Message 2"]

@pytest.mark.asyncio
async def test_send_empty_message(send, message_stack):
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_none_message(send, message_stack):
    await send(None)
    assert message_stack == [None]

@pytest.mark.asyncio
async def test_send_message_stack_persistence(send, message_stack):
    await send("First Message")
    assert message_stack == ["First Message"]
    await send("Second Message")
    assert message_stack == ["First Message", "Second Message"]