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

@pytest.mark.asyncio
async def test_send_message(app, send, message_stack):
    message = "Hello, World!"
    await send(message)
    assert message_stack == [message]

@pytest.mark.asyncio
async def test_send_multiple_messages(app, send, message_stack):
    messages = ["First message", "Second message", "Third message"]
    for msg in messages:
        await send(msg)
    assert message_stack == messages

@pytest.mark.asyncio
async def test_send_empty_message(app, send, message_stack):
    await send("")
    assert message_stack == [""]

@pytest.mark.asyncio
async def test_send_none_message(app, send, message_stack):
    with pytest.raises(TypeError):
        await send(None)

@pytest.mark.asyncio
async def test_stream_response_with_cookies(app):
    @app.route("/")
    async def test(request: Request):
        headers = Header()
        cookies = CookieJar(headers)
        cookies["test"] = "modified"
        cookies["test"] = "pass"
        response = await request.respond(
            content_type="text/csv", headers=headers
        )

        await response.send("foo,")
        await asyncio.sleep(0.001)
        await response.send("bar")

    request, response = app.test_client.get("/")
    assert response.cookies["test"] == "pass"