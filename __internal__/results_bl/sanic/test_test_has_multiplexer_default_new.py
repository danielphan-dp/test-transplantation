import sys
import multiprocessing.Event
import os.environ
import os.getpid
import typing.Any
import typing.Dict
import typing.Type
import typing.Union
from unittest.mock import Mock
import pytest
from sanic import Sanic
from sanic.compat import use_context
from sanic.worker.multiplexer import WorkerMultiplexer
from sanic.worker.state import WorkerState

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_method_with_worker_multiplexer(app: Sanic):
    app.m = WorkerMultiplexer()
    event = multiprocessing.Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    app.stop = Mock()

    with use_context("fork"):
        app.run()

    app.stop()
    assert app.stop.called
    assert event.is_set()

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_method_without_worker_multiplexer(app: Sanic):
    event = multiprocessing.Event()

    @app.main_process_start
    async def setup(app, _):
        app.shared_ctx.event = event

    app.stop = Mock()

    with use_context("fork"):
        app.run()

    app.stop()
    assert app.stop.called
    assert not event.is_set()