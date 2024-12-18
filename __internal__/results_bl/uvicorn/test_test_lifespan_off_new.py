import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.off import LifespanOff

class TestLifespan:
    async def app(self, scope, receive, send):
        pass  # pragma: no cover

    @pytest.mark.asyncio
    async def test_lifespan_close(self):
        config = Config(app=self.app, lifespan="off")
        lifespan = LifespanOff(config)

        await lifespan.startup()
        lifespan.close()
        assert lifespan.closed is True

    @pytest.mark.asyncio
    async def test_lifespan_close_already_closed(self):
        config = Config(app=self.app, lifespan="off")
        lifespan = LifespanOff(config)

        await lifespan.startup()
        lifespan.close()
        
        with pytest.raises(AssertionError):
            lifespan.close()