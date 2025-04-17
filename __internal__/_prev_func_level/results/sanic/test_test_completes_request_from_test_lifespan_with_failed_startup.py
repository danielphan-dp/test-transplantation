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

def test_stop_app(app, caplog: LogCaptureFixture):
    @app.get("/")
    async def handler(request):
        return empty()

    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    stop(app)

    assert ("sanic.access", 20, "") in caplog.record_tuples

    index_stopping = 0
    for idx, record in enumerate(caplog.records):
        if record.message.startswith("Stopping worker"):
            index_stopping = idx
            break
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request > index_stopping > 0

def test_stop_app_without_running(app, caplog: LogCaptureFixture):
    with caplog.at_level(logging.INFO):
        stop(app)

    assert "Stopping worker" not in caplog.text

def test_stop_app_with_active_requests(app, caplog: LogCaptureFixture):
    @app.get("/")
    async def handler(request):
        await asyncio.sleep(2)
        return empty()

    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True)

    asyncio.run(stop(app))

    assert ("sanic.access", 20, "") in caplog.record_tuples

    index_stopping = 0
    for idx, record in enumerate(caplog.records):
        if record.message.startswith("Stopping worker"):
            index_stopping = idx
            break
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request > index_stopping > 0