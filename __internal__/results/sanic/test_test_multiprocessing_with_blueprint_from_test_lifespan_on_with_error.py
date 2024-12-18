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
        app.stop_called = True
        app.stop()

    app.run(HOST, port=8000, debug=True)

    assert app.stop_called is True

def test_app_stop_no_running_app():
    app = Sanic("TestApp")
    with pytest.raises(RuntimeError):
        app.stop()