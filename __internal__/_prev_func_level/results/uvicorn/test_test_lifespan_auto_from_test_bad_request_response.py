import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

calls = []

def test_shutdown():
    async def app(scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.complete"})
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        await send({"type": "lifespan.shutdown.complete"})
        calls.append('shutdown')

    async def test():
        config = Config(app=app, lifespan="auto")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert 'shutdown' not in calls
        await lifespan.shutdown()
        assert 'shutdown' in calls

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()