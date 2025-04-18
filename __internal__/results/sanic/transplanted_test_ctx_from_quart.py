# This test file was generated from tests/test_ctx.py to test sanic/app.py through test transplantation.

import asyncio
from unittest.mock import Mock

import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import text
from sanic.router import Router
from sanic.exceptions import BadRequest
from sanic.models.handler_types import MiddlewareType
from sanic.middleware import Middleware

# Test to ensure that request context matches correctly
async def test_request_context_match():
    app = Sanic("test_app")
    router = Mock(spec=Router)
    route = Mock()
    route.extra = {}
    router.get.return_value = (route, lambda x: x, {})
    app.router = router

    request = Request(b"/", {}, "GET", app)
    await app.handle_request(request)

    assert request.route == route

# Test to ensure BadRequest is raised for invalid routes
async def test_bad_request_if_invalid_route():
    app = Sanic("test_app")
    router = Mock(spec=Router)
    router.get.side_effect = BadRequest("Invalid route")
    app.router = router

    request = Request(b"/invalid", {}, "GET", app)
    with pytest.raises(BadRequest):
        await app.handle_request(request)

# Test to ensure middleware is executed after request
async def test_after_this_request_middleware():
    app = Sanic("test_app")

    @app.middleware("request")
    async def add_header(request):
        request.ctx.added_header = "value"

    @app.route("/")
    async def handler(request):
        return text("Hello")

    request, response = await app.asgi_client.get("/")
    assert request.ctx.added_header == "value"

# Test to ensure request context is available
async def test_has_request_context():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        assert request is not None
        return text("Hello")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200

# Test to ensure app context is available
async def test_has_app_context():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        assert app is not None
        return text("Hello")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200

# Test to ensure middleware can be copied and executed in app context
async def test_copy_current_app_context():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        @app.ext.dependency
        async def within_context():
            assert app is not None

        await asyncio.ensure_future(within_context())
        return text("Hello")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200

# Test to ensure middleware can be copied and executed in request context
async def test_copy_current_request_context():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        @app.ext.dependency
        async def within_context():
            assert request is not None

        await asyncio.ensure_future(within_context())
        return text("Hello")

    request, response = await app.asgi_client.get("/")
    assert response.status == 200

# Test to ensure middleware can be copied and executed in websocket context
async def test_copy_current_websocket_context():
    app = Sanic("test_app")

    @app.websocket("/")
    async def handler(request, ws):
        @app.ext.dependency
        async def within_context():
            return request.path

        data = await asyncio.ensure_future(within_context())
        await ws.send(data)

    test_client = app.test_client()
    async with test_client.websocket("/") as test_websocket:
        data = await test_websocket.receive()
    assert data == "/"