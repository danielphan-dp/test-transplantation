import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

calls = []

def test_lifespan_shutdown():
    async def app(scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.complete"})
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        await send({"type": "lifespan.shutdown.complete"})

    async def test():
        config = Config(app=app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert not lifespan.error_occured
        assert lifespan.should_exit
        await lifespan.shutdown()
        assert 'shutdown' in calls

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()

def test_lifespan_shutdown_with_error():
    async def app(scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.complete"})
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        await send({"type": "lifespan.shutdown.failed", "message": "shutdown error"})

    async def test():
        config = Config(app=app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert not lifespan.error_occured
        await lifespan.shutdown()
        assert lifespan.shutdown_failed
        assert lifespan.should_exit

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()