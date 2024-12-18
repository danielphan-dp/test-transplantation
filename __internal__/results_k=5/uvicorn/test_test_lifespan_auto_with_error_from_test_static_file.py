import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

class TestLifespanClose:
    async def app(self, scope, receive, send):
        assert scope["type"] == "http"

    async def test_close_method(self):
        config = Config(app=self.app, lifespan="auto")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert not lifespan.should_exit
        
        lifespan.close()
        assert lifespan.closed
        with pytest.raises(AssertionError):
            lifespan.close()  # Should raise an error since it's already closed

        await lifespan.shutdown()