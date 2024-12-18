import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

def test_lifespan_startup_edge_cases():
    startup_complete = False
    shutdown_complete = False

    async def app(scope, receive, send):
        nonlocal startup_complete, shutdown_complete
        message = await receive()
        assert message["type"] == "lifespan.startup"
        startup_complete = True
        await send({"type": "lifespan.startup.complete"})
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        shutdown_complete = True
        await send({"type": "lifespan.shutdown.complete"})

    async def test():
        config = Config(app=app, lifespan="on")
        lifespan = LifespanOn(config)

        assert not startup_complete
        assert not shutdown_complete
        await lifespan.startup()
        assert startup_complete
        assert not shutdown_complete
        await lifespan.shutdown()
        assert startup_complete
        assert shutdown_complete

        # Additional edge case: startup called multiple times
        startup_complete = False
        await lifespan.startup()
        assert startup_complete

        # Additional edge case: shutdown called without startup
        shutdown_complete = False
        await lifespan.shutdown()
        assert not shutdown_complete

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()