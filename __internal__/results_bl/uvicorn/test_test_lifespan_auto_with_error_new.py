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
        assert not lifespan.closed
        lifespan.close()
        assert lifespan.closed

    async def test_close_method_when_already_closed(self):
        config = Config(app=self.app, lifespan="auto")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        lifespan.close()
        with pytest.raises(AssertionError):
            lifespan.close()