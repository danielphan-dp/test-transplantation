import asyncio
import logging
from typing import Callable, List
import pytest
from sanic import Sanic
from sanic.exceptions import ServerError
from sanic.response import text

@pytest.fixture
def message_stack():
    return []

@pytest.fixture
def send(message_stack):
    async def _send(message):
        message_stack.append(message)
    return _send

@pytest.mark.asyncio
async def test_send_function(app: Sanic, send, message_stack):
    message = "Test message"
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_empty_message(app: Sanic, send, message_stack):
    message = ""
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_multiple_messages(app: Sanic, send, message_stack):
    messages = ["First message", "Second message", "Third message"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

@pytest.mark.asyncio
async def test_send_none_message(app: Sanic, send, message_stack):
    message = None
    await send(message)
    assert message_stack == [message]