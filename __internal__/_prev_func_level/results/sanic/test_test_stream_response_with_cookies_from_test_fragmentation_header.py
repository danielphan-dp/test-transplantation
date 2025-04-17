import asyncio
import pytest
from sanic import Sanic, Request
from sanic.cookies import CookieJar
from sanic.compat import Header

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

@app.route("/")
async def test(request: Request):
    headers = Header()
    cookies = CookieJar(headers)
    cookies["test"] = "initial"
    response = await request.respond(content_type="text/csv", headers=headers)
    await response.send("foo,")
    await asyncio.sleep(0.001)
    await response.send("bar")

@pytest.mark.asyncio
async def test_send_function(send, message_stack):
    await send("Hello, World!")
    assert message_stack == ["Hello, World!"]

@pytest.mark.asyncio
async def test_stream_response_with_cookies(app):
    request, response = app.test_client.get("/")
    assert response.cookies["test"] == "initial"

@pytest.mark.asyncio
async def test_send_multiple_messages(send, message_stack):
    await send("Message 1")
    await send("Message 2")
    assert message_stack == ["Message 1", "Message 2"]

@pytest.mark.asyncio
async def test_send_empty_message(send, message_stack):
    await send("")
    assert message_stack == [""]