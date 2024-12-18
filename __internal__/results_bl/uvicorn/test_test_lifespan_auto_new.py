import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

calls = []

def test_shutdown():
    shutdown_complete = False

    async def app(scope, receive, send):
        nonlocal shutdown_complete
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        shutdown_complete = True
        await send({"type": "lifespan.shutdown.complete"})

    async def test():
        config = Config(app=app, lifespan="auto")
        lifespan = LifespanOn(config)

        await lifespan.shutdown()
        assert shutdown_complete
        assert 'shutdown' in calls

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()

def test_shutdown_without_startup():
    shutdown_complete = False

    async def app(scope, receive, send):
        nonlocal shutdown_complete
        message = await receive()
        if message["type"] == "lifespan.shutdown":
            shutdown_complete = True
            await send({"type": "lifespan.shutdown.complete"})

    async def test():
        config = Config(app=app, lifespan="auto")
        lifespan = LifespanOn(config)

        await lifespan.shutdown()
        assert not shutdown_complete
        assert 'shutdown' not in calls

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()