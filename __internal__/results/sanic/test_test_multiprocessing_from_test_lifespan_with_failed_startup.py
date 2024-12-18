import pytest
import signal
import sys
from sanic import Sanic
from sanic_testing.testing import HOST

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform, we have to come up with another timeout strategy to test these')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop(app):
    """Tests that the app stops correctly"""
    app_started = False

    @app.after_server_start
    async def start(app):
        nonlocal app_started
        app_started = True

    @app.after_server_stop
    async def stop(app):
        assert app_started is True

    app.run(HOST, port=8000, debug=True)
    app.stop()

    assert not app_started  # Ensure the app has stopped

def test_app_stop_with_exception(app):
    """Tests that the app can handle exceptions during stop"""
    app_started = False

    @app.after_server_start
    async def start(app):
        nonlocal app_started
        app_started = True

    @app.after_server_stop
    async def stop(app):
        raise RuntimeError("Forced exception during stop")

    app.run(HOST, port=8000, debug=True)
    with pytest.raises(RuntimeError, match="Forced exception during stop"):
        app.stop()