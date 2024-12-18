import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

calls = []

def test_startup_method():
    async def app(scope, receive, send):
        message = await receive()
        if message["type"] == "lifespan.startup":
            calls.append('startup')
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})

    async def test():
        config = Config(app=app, lifespan="on")
        lifespan = LifespanOn(config)

        assert 'startup' not in calls
        await lifespan.startup()
        assert 'startup' in calls

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()

def test_startup_multiple_calls():
    async def app(scope, receive, send):
        message = await receive()
        if message["type"] == "lifespan.startup":
            calls.append('startup')
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})

    async def test():
        config = Config(app=app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        await lifespan.startup()  # Call startup again
        assert calls.count('startup') == 2

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()

def test_startup_without_shutdown():
    async def app(scope, receive, send):
        message = await receive()
        if message["type"] == "lifespan.startup":
            calls.append('startup')
            await send({"type": "lifespan.startup.complete"})

    async def test():
        config = Config(app=app, lifespan="on")
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert 'startup' in calls
        # No shutdown call, so we don't check for shutdown completion

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()