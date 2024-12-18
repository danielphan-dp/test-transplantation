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
async def test_shutdown():
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
async def test_shutdown_without_startup():
    global calls
    calls.clear()
    
    config = Config(app=app, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.shutdown()
    assert "shutdown" in calls

@pytest.mark.asyncio
async def test_multiple_shutdown_calls():
    global calls
    calls.clear()
    
    config = Config(app=app, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.startup()
    assert "startup" in calls
    await lifespan.shutdown()
    await lifespan.shutdown()
    assert calls.count("shutdown") == 1

@pytest.mark.asyncio
async def test_shutdown_with_exception_handling():
    global calls
    calls.clear()
    
    async def faulty_app(scope, receive, send):
        message = await receive()
        if message["type"] == "lifespan.startup":
            calls.append("startup")
            await send({"type": "lifespan.startup.complete"})
        message = await receive()
        if message["type"] == "lifespan.shutdown":
            calls.append("shutdown")
            raise RuntimeError("Shutdown error")

    config = Config(app=faulty_app, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.startup()
    assert "startup" in calls
    with pytest.raises(RuntimeError, match="Shutdown error"):
        await lifespan.shutdown()