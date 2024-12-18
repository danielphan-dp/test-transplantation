import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(scope, receive, send):
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
        assert lifespan.closed is True

    async def test_close_already_closed(self):
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

    def run_tests(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.test_close_not_closed())
        loop.run_until_complete(self.test_close_already_closed())
        loop.run_until_complete(self.test_close_without_startup())
        loop.close()

if __name__ == "__main__":
    test_instance = TestLifespanClose()
    test_instance.run_tests()