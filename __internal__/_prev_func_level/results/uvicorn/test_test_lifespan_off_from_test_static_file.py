import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.off import LifespanOff

class TestLifespanOff:
    async def app(self, scope, receive, send):
        pass  # pragma: no cover

    async def test_lifespan_close(self):
        config = Config(app=self.app, lifespan="off")
        lifespan = LifespanOff(config)

        # Ensure the lifespan is not closed initially
        assert not lifespan.closed

        # Call the close method
        lifespan.close()

        # Check that the lifespan is now closed
        assert lifespan.closed

    async def test_lifespan_close_when_already_closed(self):
        config = Config(app=self.app, lifespan="off")
        lifespan = LifespanOff(config)

        # Close the lifespan first
        lifespan.close()

        # Attempt to close again and check for assertion
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_lifespan_close_multiple_calls(self):
        config = Config(app=self.app, lifespan="off")
        lifespan = LifespanOff(config)

        # Close the lifespan
        lifespan.close()

        # Check that it is closed
        assert lifespan.closed

        # Call close again and ensure it does not raise an error
        lifespan.close()

    def run_tests(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.test_lifespan_close())
        loop.run_until_complete(self.test_lifespan_close_when_already_closed())
        loop.run_until_complete(self.test_lifespan_close_multiple_calls())
        loop.close()