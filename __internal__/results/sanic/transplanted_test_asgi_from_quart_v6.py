# Transplanted from tests/test_asgi.py to test the functionality in sanic/app.py

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.app import ASGIApp
from sanic.asgi import Lifespan


@pytest.mark.asyncio
async def test_handle_request():
    # Create a mock Sanic app
    app = Sanic("test_app")

    # Define a simple handler
    @app.route("/")
    async def handler(request):
        return HTTPResponse("Hello, world!")

    # Create a mock request
    request = Request(b"/", {}, app)

    # Call the handle_request method
    await app.handle_request(request)

    # Assert that the response is as expected
    assert request.stream.response.body == b"Hello, world!"


@pytest.mark.asyncio
async def test_handle_exception():
    # Create a mock Sanic app
    app = Sanic("test_app")

    # Define a handler that raises an exception
    @app.route("/")
    async def handler(request):
        raise ValueError("An error occurred")

    # Create a mock request
    request = Request(b"/", {}, app)

    # Call the handle_request method and handle exception
    await app.handle_request(request)

    # Assert that the response is a 500 error
    assert request.stream.response.status == 500


@pytest.mark.asyncio
async def test_asgi_lifespan():
    # Create a mock Sanic app
    app = Sanic("test_app")

    # Create a mock scope
    scope = {"type": "lifespan"}

    # Create a mock receive and send
    async def receive():
        return {"type": "lifespan.startup"}

    async def send(message):
        assert message["type"] == "lifespan.startup.complete"

    # Create an ASGI Lifespan instance
    lifespan = Lifespan(app, scope, receive, send)

    # Call the lifespan
    await lifespan()


@pytest.mark.asyncio
async def test_asgi_app():
    # Create a mock Sanic app
    app = Sanic("test_app")

    # Create a mock scope
    scope = {"type": "http"}

    # Create a mock receive and send
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        assert message["type"] == "http.response.start"

    # Create an ASGI App instance
    asgi_app = await ASGIApp.create(app, scope, receive, send)

    # Call the ASGI app
    await asgi_app()


@pytest.mark.asyncio
async def test_dispatch_event():
    # Create a mock Sanic app
    app = Sanic("test_app")

    # Define a signal handler
    @app.signal("test.event")
    async def handler(**context):
        assert context["data"] == "test"

    # Dispatch the event
    await app.dispatch("test.event", context={"data": "test"})


@pytest.mark.asyncio
async def test_add_task():
    # Create a mock Sanic app
    app = Sanic("test_app")

    # Define a simple task
    async def task():
        await asyncio.sleep(0.1)
        return "task completed"

    # Add the task to the app
    app.add_task(task(), name="test_task")

    # Retrieve the task
    task = app.get_task("test_task")

    # Assert that the task is not None
    assert task is not None

    # Wait for the task to complete
    result = await task

    # Assert that the task result is as expected
    assert result == "task completed"