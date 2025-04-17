import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(self, scope, receive, send):
        pass

    async def test_close_not_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)
        lifespan.closed = False
        
        lifespan.close()
        
        assert lifespan.closed

    async def test_close_already_closed(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)
        lifespan.closed = True
        
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_close_multiple_calls(self):
        config = Config(app=self.app, lifespan="on")
        lifespan = LifespanOn(config)
        lifespan.closed = False
        
        lifespan.close()
        assert lifespan.closed
        
        with pytest.raises(AssertionError):
            lifespan.close()

    def run_tests(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.test_close_not_closed())
        loop.run_until_complete(self.test_close_already_closed())
        loop.run_until_complete(self.test_close_multiple_calls())
        loop.close()

if __name__ == "__main__":
    test = TestLifespanClose()
    test.run_tests()