import asyncio
import os
import signal
import pytest
from types import SimpleNamespace

class MockApp:
    def __init__(self):
        self.state = SimpleNamespace()
        self.state.is_stopping = False

    def stop(self):
        assert not self.state.is_stopping
        self.state.is_stopping = True

async def test_stop_method():
    app = MockApp()
    app.stop()
    assert app.state.is_stopping

async def test_stop_method_when_already_stopping():
    app = MockApp()
    app.state.is_stopping = True
    with pytest.raises(AssertionError):
        app.stop()

async def test_stop_method_with_signal():
    app = MockApp()
    loop = asyncio.get_event_loop()
    app.stop()
    await asyncio.sleep(0.1)
    os.kill(os.getpid(), signal.SIGINT)
    await asyncio.sleep(0.1)
    assert app.state.is_stopping

@pytest.mark.asyncio
async def test_multiple_stops():
    app = MockApp()
    app.stop()
    assert app.state.is_stopping
    app.stop()  # Should not raise an error
    assert app.state.is_stopping

@pytest.mark.asyncio
async def test_stop_method_in_event_loop():
    app = MockApp()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    await loop.run_until_complete(test_stop_method())
    await loop.run_until_complete(test_stop_method_when_already_stopping())
    await loop.run_until_complete(test_stop_method_with_signal())
    await loop.run_until_complete(test_multiple_stops())
    loop.close()