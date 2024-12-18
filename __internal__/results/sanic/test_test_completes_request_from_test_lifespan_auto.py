import asyncio
import logging
import pytest
from pytest import LogCaptureFixture
from sanic import Sanic
from sanic.response import empty
from sanic import stop

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_app_stop_triggers_shutdown(app, caplog: LogCaptureFixture):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.get("/")
    async def handler(request):
        return empty()

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        await asyncio.sleep(0.5)
        stop(app)

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    assert ("sanic.access", 20, "") in caplog.record_tuples

    index_stopping = 0
    for idx, record in enumerate(caplog.records):
        if record.message.startswith("Stopping worker"):
            index_stopping = idx
            break
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request > index_stopping > 0

def test_app_stop_no_active_requests(app, caplog: LogCaptureFixture):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        stop(app)

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    assert ("sanic.access", 20, "") not in caplog.record_tuples

def test_app_stop_with_long_running_request(app, caplog: LogCaptureFixture):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 2

    @app.get("/")
    async def handler(request):
        await asyncio.sleep(3)
        return empty()

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        await asyncio.sleep(1)
        stop(app)

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    assert ("sanic.access", 20, "") in caplog.record_tuples

    index_stopping = 0
    for idx, record in enumerate(caplog.records):
        if record.message.startswith("Stopping worker"):
            index_stopping = idx
            break
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request > index_stopping > 0