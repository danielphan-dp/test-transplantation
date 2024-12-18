import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.complete"})
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        await send({"type": "lifespan.shutdown.complete"})

    async def test_close_method(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert not lifespan.closed
        lifespan.close()
        assert lifespan.closed

    async def test_close_when_already_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_close_without_startup(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        with pytest.raises(AssertionError):
            lifespan.close()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test_close_method())
    loop.run_until_complete(test_close_when_already_closed())
    loop.run_until_complete(test_close_without_startup())
    loop.close()