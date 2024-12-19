import asyncio
import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.cookies import CookieJar

@pytest.fixture
def message_stack():
    return []

@pytest.fixture
def send(message_stack):
    async def _send(message):
        message_stack.append(message)
    return _send

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@pytest.mark.asyncio
async def test_send_function(app, send):
    message_stack = []
    await send("test message 1")
    await send("test message 2")
    assert message_stack == ["test message 1", "test message 2"]

@pytest.mark.asyncio
async def test_send_empty_message(app, send):
    message_stack = []
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_none_message(app, send):
    message_stack = []
    await send(None)
    assert message_stack == [None]

@pytest.mark.asyncio
async def test_send_multiple_messages(app, send):
    message_stack = []
    await send("message 1")
    await send("message 2")
    await send("message 3")
    assert message_stack == ["message 1", "message 2", "message 3"]