import pytest
from sanic import Sanic, Request, Websocket

@pytest.fixture
def message_stack():
    return []

@pytest.mark.asyncio
@pytest.mark.parametrize("message", ["test message", "", None])
async def test_send_message(send, message, message_stack):
    await send(message)
    if message is None:
        assert message_stack == []
    else:
        assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    messages = ["first message", "second message"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

@pytest.mark.asyncio
async def test_send_empty_message(send, message_stack):
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_none_message(send, message_stack):
    await send(None)
    assert message_stack == []