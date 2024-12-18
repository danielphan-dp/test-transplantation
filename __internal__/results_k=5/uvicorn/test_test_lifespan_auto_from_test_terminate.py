import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

calls = []

async def app(scope, receive, send):
    message = await receive()
    if message["type"] == "lifespan.startup":
        calls.append("startup")
        await send({"type": "lifespan.startup.complete"})
    message = await receive()
    if message["type"] == "lifespan.shutdown":
        calls.append("shutdown")
        await send({"type": "lifespan.shutdown.complete"})

@pytest.mark.asyncio
async def test_lifespan_shutdown():
    global calls
    calls.clear()
    
    config = Config(app=app, lifespan="auto")
    lifespan = LifespanOn(config)

    assert "shutdown" not in calls
    await lifespan.startup()
    assert "startup" in calls
    await lifespan.shutdown()
    assert "shutdown" in calls

@pytest.mark.asyncio
async def test_lifespan_shutdown_no_startup():
    global calls
    calls.clear()
    
    async def faulty_app(scope, receive, send):
        message = await receive()
        if message["type"] == "lifespan.shutdown":
            calls.append("shutdown")
            await send({"type": "lifespan.shutdown.complete"})

    config = Config(app=faulty_app, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.shutdown()
    assert "shutdown" in calls

@pytest.mark.asyncio
async def test_lifespan_shutdown_with_exception():
    global calls
    calls.clear()
    
    async def app_with_exception(scope, receive, send):
        message = await receive()
        if message["type"] == "lifespan.startup":
            calls.append("startup")
            await send({"type": "lifespan.startup.complete"})
        message = await receive()
        if message["type"] == "lifespan.shutdown":
            raise RuntimeError("Shutdown failed")

    config = Config(app=app_with_exception, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.startup()
    assert "startup" in calls
    with pytest.raises(RuntimeError, match="Shutdown failed"):
        await lifespan.shutdown()