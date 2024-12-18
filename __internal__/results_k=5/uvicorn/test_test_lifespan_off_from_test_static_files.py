import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.off import LifespanOff

class TestLifespanOff:
    async def app(self, scope, receive, send):
        pass  # pragma: no cover

    async def test_close_method(self):
        config = Config(app=self.app, lifespan="off")
        lifespan = LifespanOff(config)

        # Ensure the lifespan is not closed initially
        assert not lifespan.closed

        # Call the close method
        lifespan.close()

        # Check that the lifespan is now closed
        assert lifespan.closed

    async def test_close_method_when_already_closed(self):
        config = Config(app=self.app, lifespan="off")
        lifespan = LifespanOff(config)

        # Close the lifespan first
        lifespan.close()

        # Attempt to close again and check for assertion
        with pytest.raises(AssertionError):
            lifespan.close()

    def run_tests(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.test_close_method())
        loop.run_until_complete(self.test_close_method_when_already_closed())
        loop.close()