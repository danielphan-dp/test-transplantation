import pytest
import signal
import sys
from sanic import Sanic
from sanic_testing.testing import HOST

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop(app: Sanic):
    app.stop_called = False

    @app.after_server_start
    async def after_start(app):
        await asyncio.sleep(1)
        app.stop()
        app.stop_called = True

    app.run(HOST, debug=True)

    assert app.stop_called is True

def test_app_stop_no_active_tasks(app: Sanic):
    app.stop_called = False

    @app.after_server_start
    async def after_start(app):
        await asyncio.sleep(1)
        app.stop()
        app.stop_called = True

    app.run(HOST, debug=True)

    assert app.stop_called is True

def test_app_stop_with_active_tasks(app: Sanic):
    app.stop_called = False
    task_completed = False

    @app.after_server_start
    async def after_start(app):
        await asyncio.sleep(1)
        app.stop()
        app.stop_called = True

    @app.listener('before_server_stop')
    async def before_stop(app):
        nonlocal task_completed
        await asyncio.sleep(0.5)
        task_completed = True

    app.run(HOST, debug=True)

    assert app.stop_called is True
    assert task_completed is True