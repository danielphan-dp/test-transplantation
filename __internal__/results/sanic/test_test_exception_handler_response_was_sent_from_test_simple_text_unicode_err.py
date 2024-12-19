import logging
from typing import List, Callable
import pytest
from sanic import Sanic, Request
from sanic.response import text
from sanic.exceptions import ServerError

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
async def test_send_message(app, send, message_stack):
    message = "Hello, World!"
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_empty_message(app, send, message_stack):
    message = ""
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_multiple_messages(app, send, message_stack):
    messages = ["First message", "Second message", "Third message"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

@pytest.mark.asyncio
async def test_send_non_string_message(app, send, message_stack):
    message = b"Binary message"
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_none_message(app, send, message_stack):
    message = None
    await send(message)
    assert message_stack == [message]