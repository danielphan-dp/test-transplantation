import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

calls = []

async def app(scope, receive, send):
    message = await receive()
    assert message["type"] == "lifespan.startup"
    calls.append("startup")
    await send({"type": "lifespan.startup.complete"})
    message = await receive()
    assert message["type"] == "lifespan.shutdown"
    calls.append("shutdown")
    await send({"type": "lifespan.shutdown.complete"})

@pytest.mark.asyncio
async def test_lifespan_shutdown():
    config = Config(app=app, lifespan="auto")
    lifespan = LifespanOn(config)

    assert "shutdown" not in calls
    await lifespan.startup()
    assert "startup" in calls
    await lifespan.shutdown()
    assert "shutdown" in calls

@pytest.mark.asyncio
async def test_lifespan_shutdown_without_startup():
    config = Config(app=app, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.shutdown()
    assert "shutdown" in calls

@pytest.mark.asyncio
async def test_lifespan_shutdown_multiple_calls():
    config = Config(app=app, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.startup()
    await lifespan.shutdown()
    await lifespan.shutdown()
    assert calls.count("shutdown") == 2

@pytest.mark.asyncio
async def test_lifespan_shutdown_with_exception():
    async def app_with_exception(scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.complete"})
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        raise RuntimeError("Shutdown failed")

    config = Config(app=app_with_exception, lifespan="auto")
    lifespan = LifespanOn(config)

    await lifespan.startup()
    with pytest.raises(RuntimeError, match="Shutdown failed"):
        await lifespan.shutdown()