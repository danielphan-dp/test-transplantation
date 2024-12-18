import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

@pytest.mark.parametrize('mode', ('auto', 'on'))
@pytest.mark.parametrize('raise_exception', (True, False))
async def test_lifespan_close_method(mode, raise_exception, caplog):
    async def app(scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.complete"})
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        await send({"type": "lifespan.shutdown.failed", "message": "the lifespan event failed"})

        if raise_exception:
            raise RuntimeError()

    async def test():
        config = Config(app=app, lifespan=mode)
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert not lifespan.startup_failed
        await lifespan.shutdown()
        assert lifespan.shutdown_failed
        assert lifespan.error_occured is raise_exception
        assert lifespan.should_exit

        if not lifespan.shutdown_failed:
            lifespan.close()
            assert lifespan.closed

    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    error_messages = [
        record.message for record in caplog.records if record.name == "uvicorn.error" and record.levelname == "ERROR"
    ]
    assert "the lifespan event failed" in error_messages.pop(0)
    assert "Application shutdown failed. Exiting." in error_messages.pop(0)
    loop.close()