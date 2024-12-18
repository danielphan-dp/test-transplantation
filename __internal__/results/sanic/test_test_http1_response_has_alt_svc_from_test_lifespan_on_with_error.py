import sys
import pytest
from sanic import Sanic
from sanic.response import empty

@pytest.mark.skipif(sys.version_info < (3, 9), reason='Not supported in 3.7')
def test_app_stop():
    app = Sanic("TestAppStop")

    @app.get("/")
    async def handler(_):
        return empty()

    @app.after_server_start
    async def start_server(*_):
        await app.stop()

    app.prepare(port=8000)
    app.run()

    assert not app.is_running  # Ensure the app has stopped after the call to stop()