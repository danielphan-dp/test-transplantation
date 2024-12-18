import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def test_close_method(self):
        config = Config(app=lambda scope, receive, send: None, lifespan="on")
        lifespan = LifespanOn(config)

        # Ensure the lifespan is not closed initially
        assert not lifespan.closed

        # Call the close method
        lifespan.close()

        # Check that the lifespan is now closed
        assert lifespan.closed

    async def test_close_method_when_already_closed(self):
        config = Config(app=lambda scope, receive, send: None, lifespan="on")
        lifespan = LifespanOn(config)

        # Close the lifespan first
        lifespan.close()

        # Attempt to close again and check for assertion
        with pytest.raises(AssertionError):
            lifespan.close()

    async def test_close_method_with_multiple_calls(self):
        config = Config(app=lambda scope, receive, send: None, lifespan="on")
        lifespan = LifespanOn(config)

        # Close the lifespan
        lifespan.close()
        
        # Ensure it is closed
        assert lifespan.closed

        # Call close again and check for assertion
        with pytest.raises(AssertionError):
            lifespan.close()

    def run_tests(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.test_close_method())
        loop.run_until_complete(self.test_close_method_when_already_closed())
        loop.run_until_complete(self.test_close_method_with_multiple_calls())
        loop.close()