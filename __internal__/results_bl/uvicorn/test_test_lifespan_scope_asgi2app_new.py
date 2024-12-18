import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def test_close_method(self):
        config = Config(app=lambda scope: None, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        assert lifespan.closed is True

    async def test_close_method_when_already_closed(self):
        config = Config(app=lambda scope: None, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        
        with pytest.raises(AssertionError):
            lifespan.close()

loop = asyncio.new_event_loop()
loop.run_until_complete(TestLifespanClose().test_close_method())
loop.run_until_complete(TestLifespanClose().test_close_method_when_already_closed())
loop.close()