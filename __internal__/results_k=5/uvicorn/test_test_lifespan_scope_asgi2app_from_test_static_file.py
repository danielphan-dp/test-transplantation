import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class MockApp:
    def __init__(self):
        self.closed = False

    def close(self):
        assert not self.closed
        self.closed = True

@pytest.mark.asyncio
async def test_close_method():
    app = MockApp()
    app.close()
    assert app.closed is True

@pytest.mark.asyncio
async def test_close_method_already_closed():
    app = MockApp()
    app.close()
    with pytest.raises(AssertionError):
        app.close()