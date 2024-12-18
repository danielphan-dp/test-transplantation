import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(self, scope, receive, send):
        assert scope["type"] == "http"

    async def test_close_method(self):
        config = Config(app=self.app, lifespan="auto")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert not lifespan.should_exit
        
        lifespan.close()
        assert lifespan.closed
        with pytest.raises(AssertionError):
            lifespan.close()  # Attempting to close again should raise an error

    async def test_close_method_when_already_closed(self):
        config = Config(app=self.app, lifespan="auto")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        
        with pytest.raises(AssertionError):
            lifespan.close()  # Ensure that closing again raises an error

loop = asyncio.new_event_loop()
loop.run_until_complete(TestLifespanClose().test_close_method())
loop.run_until_complete(TestLifespanClose().test_close_method_when_already_closed())
loop.close()