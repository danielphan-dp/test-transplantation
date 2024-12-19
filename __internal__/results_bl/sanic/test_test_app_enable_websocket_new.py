import pytest
from sanic import Sanic

@pytest.fixture
def message_stack():
    return []

@pytest.mark.parametrize('message', ['Hello, World!', '', None])
async def test_send_message(message_stack, message):
    send = send(message_stack)
    await send(message)
    if message is None:
        assert len(message_stack) == 0
    else:
        assert message_stack[-1] == message
        assert len(message_stack) == 1

@pytest.mark.parametrize('message', ['Test message', 'Another message'])
async def test_send_multiple_messages(message_stack, message):
    send = send(message_stack)
    await send(message)
    await send("Second message")
    assert message_stack == [message, "Second message"]