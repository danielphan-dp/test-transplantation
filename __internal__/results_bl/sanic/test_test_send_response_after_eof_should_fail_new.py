import pytest
from sanic import Sanic
from sanic.response import HTTPResponse

@pytest.fixture
def message_stack():
    return []

@pytest.fixture
def send(message_stack):
    async def _send(message):
        message_stack.append(message)
    return _send

def test_send_message_before_eof(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool], send):
    @app.get("/")
    async def handler(request: Request):
        response = await request.respond()
        await send("hello, ")
        await response.eof()
        await send("world")

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/")
        assert "hello, " in response.text
        assert not message_in_records(caplog.records, "Response stream was ended, no more response data is allowed to be sent.")

def test_send_message_after_eof_should_fail(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool], send):
    @app.get("/")
    async def handler(request: Request):
        response = await request.respond()
        await response.eof()
        await send("foo, ")

    error_msg = "Response stream was ended, no more response data is allowed to be sent."

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/")
        assert message_in_records(caplog.records, error_msg)

def test_send_multiple_messages_before_eof(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool], send):
    @app.get("/")
    async def handler(request: Request):
        response = await request.respond()
        await send("first, ")
        await send("second, ")
        await response.eof()

    with caplog.at_level(ERROR):
        _, response = app.test_client.get("/")
        assert "first, " in response.text
        assert "second, " in response.text
        assert not message_in_records(caplog.records, "Response stream was ended, no more response data is allowed to be sent.")