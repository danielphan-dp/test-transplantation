import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(self, scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.complete"})
        scope["state"]["foo"] = 123
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        await send({"type": "lifespan.shutdown.complete"})

    async def test_close_not_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert lifespan.state == {"foo": 123}
        lifespan.close()
        assert lifespan.closed

    async def test_close_already_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_close_state(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        assert lifespan.state == {"foo": 123}

loop = asyncio.new_event_loop()
loop.run_until_complete(TestLifespanClose().test_close_not_closed())
loop.run_until_complete(TestLifespanClose().test_close_already_closed())
loop.run_until_complete(TestLifespanClose().test_close_state())
loop.close()