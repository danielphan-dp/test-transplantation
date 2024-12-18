import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(self, scope, receive, send):
        pass

    async def test_close_method_not_called_when_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        lifespan.closed = True
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_close_method_successful_call(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        lifespan.closed = False
        lifespan.close()
        assert lifespan.closed

    async def test_close_method_called_twice(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)

        lifespan.closed = False
        lifespan.close()
        with pytest.raises(AssertionError):
            lifespan.close()

    def run_tests(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.test_close_method_not_called_when_closed())
        loop.run_until_complete(self.test_close_method_successful_call())
        loop.run_until_complete(self.test_close_method_called_twice())
        loop.close()

if __name__ == "__main__":
    test_instance = TestLifespanClose()
    test_instance.run_tests()