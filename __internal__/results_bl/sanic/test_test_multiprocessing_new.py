import logging
import multiprocessing
import random
import signal
import sys
import asyncio
import pytest
from sanic_testing.testing import HOST
from sanic import Blueprint
from sanic.text import text
from sanic.compat import use_context
from sanic.log import logger

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform, we have to come up with another timeout strategy to test these')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_method(app, port):
    """Tests that the stop method correctly stops the app"""
    app.run(HOST, port, debug=True)
    app.stop()
    assert app.is_stopped is True

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform, we have to come up with another timeout strategy to test these')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_multiple_times(app, port):
    """Tests that calling stop multiple times does not raise an error"""
    app.run(HOST, port, debug=True)
    for _ in range(5):
        app.stop()
    assert app.is_stopped is True

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform, we have to come up with another timeout strategy to test these')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_before_start(app, port):
    """Tests that calling stop before the app starts does not raise an error"""
    app.stop()
    assert app.is_stopped is True

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform, we have to come up with another timeout strategy to test these')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_with_active_children(app, port):
    """Tests that the app stops correctly when there are active children"""
    num_workers = random.choice(range(2, multiprocessing.cpu_count() * 2 + 1))
    process_list = set()

    @app.after_server_start
    async def shutdown(app):
        await asyncio.sleep(2.1)
        app.stop()

    def stop_on_alarm(*args):
        for process in multiprocessing.active_children():
            process_list.add(process.pid)

    signal.signal(signal.SIGALRM, stop_on_alarm)
    signal.alarm(2)
    with use_context("fork"):
        app.run(HOST, port, workers=num_workers, debug=True)

    assert len(process_list) == num_workers + 1
    app.stop()
    assert app.is_stopped is True