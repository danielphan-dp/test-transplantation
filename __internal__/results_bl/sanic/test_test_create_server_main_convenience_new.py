import asyncio
import logging
import pytest
from sanic import Sanic

@pytest.mark.asyncio
async def test_main_process_start_logging(app: Sanic, caplog):
    app.main_process_start(lambda *_: ...)
    with caplog.at_level(logging.INFO):
        await app.main_process_start(app, asyncio.get_event_loop())
    assert ("sanic.root", 30, "main_process_start") in caplog.record_tuples

@pytest.mark.asyncio
async def test_main_process_start_no_logging(app: Sanic, caplog):
    app.main_process_start(lambda *_: ...)
    with caplog.at_level(logging.WARNING):
        await app.main_process_start(app, asyncio.get_event_loop())
    assert not any(record for record in caplog.record_tuples if record[2] == "main_process_start")

@pytest.mark.asyncio
async def test_main_process_start_multiple_calls(app: Sanic, caplog):
    app.main_process_start(lambda *_: ...)
    with caplog.at_level(logging.INFO):
        await app.main_process_start(app, asyncio.get_event_loop())
        await app.main_process_start(app, asyncio.get_event_loop())
    assert caplog.record_tuples.count(("sanic.root", 30, "main_process_start")) == 2