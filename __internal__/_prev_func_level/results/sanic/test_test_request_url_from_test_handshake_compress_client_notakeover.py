import pytest
from sanic import Sanic, Request, Websocket

@pytest.fixture
def message_stack():
    return []

@pytest.mark.parametrize("message", ["test message", "", None])
async def test_send_message(app: Sanic, message_stack, message):
    send = app.send
    await send(message)
    if message is None:
        assert len(message_stack) == 0
    else:
        assert message_stack[-1] == message

@pytest.mark.parametrize("message", ["test 1", "test 2", ""])
async def test_send_multiple_messages(app: Sanic, message_stack, message):
    send = app.send
    await send(message)
    await send("another message")
    assert message_stack[-2] == message
    assert message_stack[-1] == "another message"

@pytest.mark.asyncio
async def test_send_invalid_message_type(app: Sanic, message_stack):
    send = app.send
    with pytest.raises(TypeError):
        await send({"key": "value"})  # Sending a dict should raise TypeError

@pytest.mark.asyncio
async def test_send_after_close(app: Sanic, message_stack):
    send = app.send
    app.ws_proto.state = "CLOSED"
    with pytest.raises(Exception, match="Cannot write to websocket interface after it is closed."):
        await send("test message")