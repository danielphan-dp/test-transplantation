import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def test_close_method_when_not_closed(self):
        async def asgi3app(scope, receive, send):
            pass

        config = Config(app=asgi3app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        assert lifespan.closed

    async def test_close_method_when_already_closed(self):
        async def asgi3app(scope, receive, send):
            pass

        config = Config(app=asgi3app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_close_method_without_startup(self):
        async def asgi3app(scope, receive, send):
            pass

        config = Config(app=asgi3app, lifespan="on")
        lifespan = LifespanOn(config)

        with pytest.raises(AssertionError):
            lifespan.close()

loop = asyncio.new_event_loop()
loop.run_until_complete(TestLifespanClose().test_close_method_when_not_closed())
loop.run_until_complete(TestLifespanClose().test_close_method_when_already_closed())
loop.run_until_complete(TestLifespanClose().test_close_method_without_startup())
loop.close()