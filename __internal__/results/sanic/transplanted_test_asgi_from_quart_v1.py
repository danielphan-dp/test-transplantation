# This test file was generated from tests/test_asgi.py to test sanic/app.py through test transplantation.

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.app import ASGIApp
from sanic.asgi import Lifespan

@pytest.fixture
def app():
    return Sanic("test_app")

@pytest.fixture
def asgi_app(app):
    return ASGIApp(app)

@pytest.fixture
def lifespan(app):
    return Lifespan(app, {}, None, None)

@pytest.mark.asyncio
async def test_handle_request(app):
    # Test that handle_request processes a request and returns a response
    request = Request(b"/", {}, "GET", "http", "1.1", None, None, None, None, None, None)
    response = HTTPResponse("Hello, world!")
    
    async def handler(request):
        return response
    
    app.router.add("/test", handler, methods=["GET"])
    
    await app.handle_request(request)
    assert request.stream.response.body == b"Hello, world!"

@pytest.mark.asyncio
async def test_handle_exception(app):
    # Test that handle_exception processes an exception and returns a response
    request = Request(b"/", {}, "GET", "http", "1.1", None, None, None, None, None, None)
    
    async def handler(request):
        raise ValueError("Test exception")
    
    app.router.add("/test", handler, methods=["GET"])
    
    with pytest.raises(ValueError):
        await app.handle_request(request)

@pytest.mark.asyncio
async def test_asgi_lifespan_startup(lifespan):
    # Test that ASGI lifespan startup completes successfully
    async def receive():
        return {"type": "lifespan.startup"}
    
    async def send(message):
        assert message["type"] == "lifespan.startup.complete"
    
    await lifespan(receive, send)

@pytest.mark.asyncio
async def test_asgi_lifespan_shutdown(lifespan):
    # Test that ASGI lifespan shutdown completes successfully
    async def receive():
        return {"type": "lifespan.shutdown"}
    
    async def send(message):
        assert message["type"] == "lifespan.shutdown.complete"
    
    await lifespan(receive, send)

@pytest.mark.asyncio
async def test_asgi_app_call(asgi_app):
    # Test that ASGI app processes a request and returns a response
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
        "query_string": b"",
        "http_version": "1.1",
        "scheme": "http",
    }
    
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}
    
    async def send(message):
        if message["type"] == "http.response.start":
            assert message["status"] == 200
        elif message["type"] == "http.response.body":
            assert message["body"] == b"Hello, world!"
    
    asgi_app.app.router.add("/", lambda request: HTTPResponse("Hello, world!"), methods=["GET"])
    await asgi_app(scope, receive, send)