import pytest
from unittest.mock import Mock

@pytest.fixture
def message_stack():
    return []

@pytest.mark.asyncio
async def test_send_message_success(message_stack):
    send_function = send(message_stack)
    await send_function("Hello, World!")
    assert message_stack == ["Hello, World!"]

@pytest.mark.asyncio
async def test_send_multiple_messages(message_stack):
    send_function = send(message_stack)
    await send_function("Message 1")
    await send_function("Message 2")
    assert message_stack == ["Message 1", "Message 2"]

@pytest.mark.asyncio
async def test_send_empty_message(message_stack):
    send_function = send(message_stack)
    await send_function("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_none_message(message_stack):
    send_function = send(message_stack)
    await send_function(None)
    assert message_stack == [None]

@pytest.mark.asyncio
async def test_send_message_stack_order(message_stack):
    send_function = send(message_stack)
    await send_function("First")
    await send_function("Second")
    await send_function("Third")
    assert message_stack == ["First", "Second", "Third"]