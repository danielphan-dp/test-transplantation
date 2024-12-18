import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

calls = []

class MockLifespanOn(LifespanOn):
    async def shutdown(self):
        calls.append('shutdown')
        await super().shutdown()

@pytest.mark.asyncio
async def test_lifespan_shutdown():
    async def app(scope, receive, send):
        if scope["type"] != "http":
            raise RuntimeError()

    config = Config(app=app, lifespan="on")
    lifespan = MockLifespanOn(config)

    await lifespan.startup()
    assert not lifespan.error_occured
    assert not lifespan.should_exit

    await lifespan.shutdown()
    assert 'shutdown' in calls

@pytest.mark.asyncio
async def test_lifespan_shutdown_with_error():
    async def app(scope, receive, send):
        if scope["type"] != "http":
            raise RuntimeError()

    config = Config(app=app, lifespan="on")
    lifespan = MockLifespanOn(config)

    await lifespan.startup()
    lifespan.error_occured = True
    lifespan.should_exit = True

    await lifespan.shutdown()
    assert 'shutdown' in calls