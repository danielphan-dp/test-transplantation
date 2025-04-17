import base64
import secrets
import pytest
from sanic import Sanic, Request, Websocket

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
    message = "Hello, WebSocket!"
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    messages = ["Message 1", "Message 2", "Message 3"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

@pytest.mark.asyncio
async def test_send_empty_message(send, message_stack):
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_binary_message(send, message_stack):
    binary_message = b'\x00\x01\x02'
    await send(binary_message)
    assert message_stack == [binary_message]

@pytest.mark.asyncio
async def test_send_invalid_message_type(send, message_stack):
    with pytest.raises(TypeError):
        await send({"key": "value"})  # Sending a dict should raise TypeError

@pytest.mark.asyncio
async def test_ws_handler_invalid_upgrade(app: Sanic):
    @app.websocket("/ws")
    async def ws_echo_handler(request: Request, ws: Websocket):
        async for msg in ws:
            await ws.send(msg)

    ws_key = base64.b64encode(secrets.token_bytes(16)).decode("utf-8")
    invalid_upgrade_headers = {
        "Upgrade": "websocket",
        # "Connection": "Upgrade",
        "Sec-WebSocket-Key": ws_key,
        "Sec-WebSocket-Version": "13",
    }
    _, response = app.test_client.get("/ws", headers=invalid_upgrade_headers)
    assert response.status == 426