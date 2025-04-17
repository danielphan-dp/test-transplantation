import asyncio
import logging
import pytest
from sanic import Sanic

@pytest.mark.asyncio
async def test_main_process_start_logging(app: Sanic, caplog):
    @app.listener('main_process_start')
    def main_process_start(app, loop):
        logger.info('main_process_start')

    loop = asyncio.get_event_loop()
    with caplog.at_level(logging.INFO):
        await app.main_process_start(lambda *_: ...)
    
    assert ("sanic.root", 30, "main_process_start") in caplog.record_tuples

@pytest.mark.asyncio
async def test_main_process_start_multiple_calls(app: Sanic, caplog):
    @app.listener('main_process_start')
    def main_process_start(app, loop):
        logger.info('main_process_start')

    loop = asyncio.get_event_loop()
    with caplog.at_level(logging.INFO):
        await app.main_process_start(lambda *_: ...)
        await app.main_process_start(lambda *_: ...)
    
    assert caplog.record_tuples.count(("sanic.root", 30, "main_process_start")) == 2

@pytest.mark.asyncio
async def test_main_process_start_no_logging(app: Sanic, caplog):
    @app.listener('main_process_start')
    def main_process_start(app, loop):
        pass  # No logging

    loop = asyncio.get_event_loop()
    await app.main_process_start(lambda *_: ...)
    
    assert not caplog.record_tuples

@pytest.mark.asyncio
async def test_main_process_start_with_error(app: Sanic, caplog):
    @app.listener('main_process_start')
    def main_process_start(app, loop):
        raise Exception("Error during main process start")

    loop = asyncio.get_event_loop()
    with pytest.raises(Exception, match="Error during main process start"):
        await app.main_process_start(lambda *_: ...)