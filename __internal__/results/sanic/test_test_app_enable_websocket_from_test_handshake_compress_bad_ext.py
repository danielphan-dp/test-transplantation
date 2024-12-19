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
async def test_send_messages(send, message_stack, message):
    await send(message)
    if message is None:
        assert message_stack == []
    else:
        assert message_stack == [message]