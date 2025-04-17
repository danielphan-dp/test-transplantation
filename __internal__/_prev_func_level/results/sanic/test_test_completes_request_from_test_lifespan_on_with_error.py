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

def test_stop_app_without_request(app, caplog: LogCaptureFixture):
    with caplog.at_level(logging.INFO):
        stop(app)

    assert ("sanic.access", 20, "") not in caplog.record_tuples
    assert "Stopping worker" not in caplog.text

def test_stop_app_with_error_logging(app, caplog: LogCaptureFixture):
    @app.get("/")
    async def handler(request):
        raise Exception("Test Exception")

    app.config.GRACEFUL_SHUTDOWN_TIMEOUT = 1

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        await asyncio.sleep(0.5)
        stop(app)

    with caplog.at_level(logging.ERROR):
        app.run(single_process=True, access_log=True)

    assert any("Test Exception" in record.message for record in caplog.records)