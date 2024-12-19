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

@pytest.fixture
def port():
    return 8000

def test_stop_app(app, caplog: LogCaptureFixture, port):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.get("/")
    async def handler(request):
        await asyncio.sleep(0.5)
        return empty()

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True, port=port)
        stop(app)

    assert ("sanic.access", 20, "") in caplog.record_tuples

    index_stopping = 0
    for idx, record in enumerate(caplog.records):
        if record.message.startswith("Stopping worker"):
            index_stopping = idx
            break
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request > index_stopping > 0

def test_stop_app_without_request(app, caplog: LogCaptureFixture, port):
    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True, port=port)
        stop(app)

    assert ("sanic.access", 20, "") not in caplog.record_tuples

def test_stop_app_with_long_running_request(app, caplog: LogCaptureFixture, port):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.get("/")
    async def handler(request):
        await asyncio.sleep(2)
        return empty()

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True, port=port)
        stop(app)

    assert ("sanic.access", 20, "") in caplog.record_tuples

    index_stopping = 0
    for idx, record in enumerate(caplog.records):
        if record.message.startswith("Stopping worker"):
            index_stopping = idx
            break
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request > index_stopping > 0

def test_stop_app_multiple_stops(app, caplog: LogCaptureFixture, port):
    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.get("/")
    async def handler(request):
        await asyncio.sleep(0.5)
        return empty()

    with caplog.at_level(logging.INFO):
        app.run(single_process=True, access_log=True, port=port)
        stop(app)
        stop(app)

    assert ("sanic.access", 20, "") in caplog.record_tuples

    index_stopping = 0
    for idx, record in enumerate(caplog.records):
        if record.message.startswith("Stopping worker"):
            index_stopping = idx
            break
    index_request = caplog.record_tuples.index(("sanic.access", 20, ""))
    assert index_request > index_stopping > 0