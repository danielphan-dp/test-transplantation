import pytest
from sanic import Sanic, Request
from logging import ERROR, LogRecord

@pytest.fixture
def message_stack():
    return []

@pytest.fixture
def send(message_stack):
    async def _send(message):
        message_stack.append(message)
    return _send

def test_send_function(app: Sanic, caplog: LogCaptureFixture, message_in_records: Callable[[List[LogRecord], str], bool], send):
    with caplog.at_level(ERROR):
        await send("Test message 1")
        assert "Test message 1" in message_stack
        assert response.status == 200

    with caplog.at_level(ERROR):
        await send("Test message 2")
        assert "Test message 2" in message_stack
        assert response.status == 200

    with caplog.at_level(ERROR):
        await send("")
        assert "" in message_stack
        assert response.status == 200

    with caplog.at_level(ERROR):
        await send(None)
        assert None in message_stack
        assert response.status == 200

    with caplog.at_level(ERROR):
        await send("Another test message")
        assert "Another test message" in message_stack
        assert message_in_records(caplog.records, "Message sent: Another test message")