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
@pytest.mark.parametrize("message", ["Hello, World!", "", None])
async def test_send_messages(send, message, message_stack):
    if message is None:
        with pytest.raises(TypeError):
            await send(message)
    else:
        await send(message)
        assert message_stack[-1] == message

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    messages = ["First message", "Second message", "Third message"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

@pytest.mark.asyncio
async def test_send_empty_stack(send, message_stack):
    assert len(message_stack) == 0
    await send("Test message")
    assert len(message_stack) == 1
    assert message_stack[0] == "Test message"