import pytest
from sanic import Sanic, Request, Websocket

@pytest.fixture
def message_stack():
    return []

@pytest.mark.parametrize("message", ["test message", "", None])
async def test_send_message(app: Sanic, message_stack, message):
    send = app.send(message_stack)
    
    await send(message)
    
    if message is None:
        assert message_stack == []
    else:
        assert message_stack == [message]