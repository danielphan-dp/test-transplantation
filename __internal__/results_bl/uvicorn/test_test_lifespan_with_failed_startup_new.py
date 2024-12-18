import asyncio
import pytest
from uvicorn.config import Config
from uvicorn.lifespan.on import LifespanOn

@pytest.mark.parametrize('mode', ('auto', 'on'))
@pytest.mark.parametrize('raise_exception', (True, False))
async def test_shutdown_with_failed_startup(mode, raise_exception, caplog):
    async def app(scope, receive, send):
        message = await receive()
        assert message["type"] == "lifespan.startup"
        await send({"type": "lifespan.startup.failed", "message": "the lifespan event failed"})
        if raise_exception:
            raise RuntimeError()

    async def test():
        config = Config(app=app, lifespan=mode)
        lifespan = LifespanOn(config)

        await lifespan.startup()
        assert lifespan.startup_failed
        assert lifespan.error_occured is raise_exception
        assert lifespan.should_exit
        await lifespan.shutdown()
        assert 'shutdown' in calls

    calls = []
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()
    error_messages = [
        record.message for record in caplog.records if record.name == "uvicorn.error" and record.levelname == "ERROR"
    ]
    assert "the lifespan event failed" in error_messages.pop(0)
    assert "Application startup failed. Exiting." in error_messages.pop(0)