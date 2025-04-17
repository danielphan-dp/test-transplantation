import pytest
import signal
import sys
from sanic import Sanic
from sanic_testing.testing import HOST

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_functionality():
    app = Sanic("TestApp")

    @app.after_server_start
    async def after_start(app):
        await asyncio.sleep(1)
        app.stop()

    app.run(HOST, port=8000, debug=True)

    assert not app.is_running

def test_app_stop_with_no_running_process():
    app = Sanic("TestApp")
    
    with pytest.raises(RuntimeError):
        app.stop()