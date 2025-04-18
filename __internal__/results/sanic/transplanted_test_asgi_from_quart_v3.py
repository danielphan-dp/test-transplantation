# This test file was generated by adapting tests from tests/test_asgi.py to test sanic/app.py

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.app import ASGIApp
from sanic.exceptions import SanicException
from sanic.signals import Event

@pytest.fixture
def app():
    return Sanic("test_app")

@pytest.mark.asyncio
async def test_handle_exception(app):
    # Test that handle_exception properly handles exceptions and returns a response
    request = Mock(spec=Request)
    exception = SanicException("Test exception")
    
    response = await app.handle_exception(request, exception)
    
    assert isinstance(response, HTTPResponse)
    assert response.status == 500

@pytest.mark.asyncio
async def test_dispatch_event(app):
    # Test that dispatching an event works correctly
    event_name = "test.event"
    mock_handler = AsyncMock()
    
    app.signal(event_name)(mock_handler)
    
    await app.dispatch(event_name, context={"key": "value"})
    
    mock_handler.assert_awaited_once()
    mock_handler.assert_awaited_with(app, {"key": "value"})

@pytest.mark.asyncio
async def test_add_task(app):
    # Test that tasks can be added and run correctly
    async def sample_task():
        return "Task Completed"
    
    task = app.add_task(sample_task())
    
    assert task is not None
    assert await task == "Task Completed"

@pytest.mark.asyncio
async def test_get_task(app):
    # Test that tasks can be retrieved by name
    async def sample_task():
        return "Task Completed"
    
    app.add_task(sample_task(), name="sample_task")
    
    task = app.get_task("sample_task")
    
    assert task is not None
    assert await task == "Task Completed"

@pytest.mark.asyncio
async def test_cancel_task(app):
    # Test that tasks can be cancelled
    async def sample_task():
        await asyncio.sleep(10)
    
    app.add_task(sample_task(), name="sample_task")
    
    await app.cancel_task("sample_task")
    
    task = app.get_task("sample_task", raise_exception=False)
    assert task is None or task.cancelled()

@pytest.mark.asyncio
async def test_asgi_lifespan(app):
    # Test ASGI lifespan events
    asgi_app = ASGIApp(app)
    
    async def mock_receive():
        return {"type": "lifespan.startup"}
    
    mock_send = AsyncMock()
    
    await asgi_app({"type": "lifespan"}, mock_receive, mock_send)
    
    mock_send.assert_any_call({"type": "lifespan.startup.complete"})

@pytest.mark.asyncio
async def test_websocket_handler(app):
    # Test that websocket handlers are set up correctly
    @app.websocket("/ws")
    async def websocket_handler(request, ws):
        await ws.send("Hello, world!")
    
    assert app.websocket_enabled
    assert "/ws" in app.router.routes_all