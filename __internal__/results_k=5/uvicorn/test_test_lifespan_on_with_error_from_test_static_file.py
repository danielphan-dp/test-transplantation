import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(self, scope, receive, send):
        pass

    async def test_close_method_not_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)
        await lifespan.startup()
        assert not lifespan.closed
        lifespan.close()
        assert lifespan.closed

    async def test_close_method_already_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)
        await lifespan.startup()
        lifespan.close()
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_close_method_with_error(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)
        await lifespan.startup()
        lifespan.close()
        assert lifespan.closed

loop = asyncio.new_event_loop()
loop.run_until_complete(TestLifespanClose().test_close_method_not_closed())
loop.run_until_complete(TestLifespanClose().test_close_method_already_closed())
loop.run_until_complete(TestLifespanClose().test_close_method_with_error())
loop.close()