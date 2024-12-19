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
async def test_send_non_string_message(send, message_stack):
    with pytest.raises(TypeError):
        await send(123)

@pytest.mark.asyncio
async def test_send_iterable_message(send, message_stack):
    await send(["Part 1", "Part 2"])
    assert message_stack == [["Part 1", "Part 2"]]  # Assuming the implementation handles lists as a single message

@pytest.mark.asyncio
async def test_send_dict_message(send, message_stack):
    with pytest.raises(TypeError):
        await send({"key": "value"})