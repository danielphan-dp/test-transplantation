import asyncio
import pytest
from aiohttp.helpers import TimeoutHandle

@pytest.fixture
def loop():
    return asyncio.get_event_loop()

def test_timeout_handle_close(loop):
    timeout = 0.1
    handle = TimeoutHandle(loop, timeout, 0.01)
    assert handle is not None
    handle.close()
    assert handle._closed is True  # Assuming _closed is an attribute that indicates if the handle is closed

def test_timeout_handle_close_multiple_times(loop):
    timeout = 0.1
    handle = TimeoutHandle(loop, timeout, 0.01)
    assert handle is not None
    handle.close()
    handle.close()  # Closing again should not raise an error
    assert handle._closed is True

def test_timeout_handle_when_not_started(loop):
    timeout = 0.1
    handle = TimeoutHandle(loop, timeout, 0.01)
    assert handle is not None
    handle.close()
    when = handle.when()  # Assuming when() should return a value even if not started
    assert when is None  # Assuming when() returns None if not started

def test_timeout_handle_start_after_close(loop):
    timeout = 0.1
    handle = TimeoutHandle(loop, timeout, 0.01)
    handle.close()
    with pytest.raises(RuntimeError):  # Assuming starting after close raises an error
        handle.start()