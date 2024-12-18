import pytest
from uvicorn import Config
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