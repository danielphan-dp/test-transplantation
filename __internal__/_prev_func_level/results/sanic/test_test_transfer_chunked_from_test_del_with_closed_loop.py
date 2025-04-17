import pytest
from sanic_testing.reusable import ReusableClient

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
    await send("test message")
    assert message_stack == ["test message"]

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    await send("first message")
    await send("second message")
    assert message_stack == ["first message", "second message"]

@pytest.mark.asyncio
async def test_send_empty_message(send, message_stack):
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_bytes_message(send, message_stack):
    await send(b"byte message")
    assert message_stack == [b"byte message"]

@pytest.mark.asyncio
async def test_send_iterable_message(send, message_stack):
    await send(["message1", "message2"])
    assert message_stack == [["message1", "message2"]]  # Assuming send handles iterables as a single message

@pytest.mark.asyncio
async def test_send_invalid_type(send, message_stack):
    with pytest.raises(TypeError):
        await send({"key": "value"})  # Expecting TypeError for dict-like input

@pytest.mark.asyncio
async def test_send_none_message(send, message_stack):
    await send(None)
    assert message_stack == [None]  # Assuming None is a valid message to send