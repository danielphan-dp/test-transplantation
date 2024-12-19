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

@pytest.mark.skipif(os.name == 'nt', reason='windows cannot SIGINT processes')
def test_stop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_stop_method())
    loop.run_until_complete(test_stop_method_when_already_stopping())
    loop.run_until_complete(test_stop_method_with_signal())
    loop.close()