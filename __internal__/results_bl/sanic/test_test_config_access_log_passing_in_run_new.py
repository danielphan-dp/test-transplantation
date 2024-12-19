import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.mark.parametrize('access_log', (True, False))
def test_stop_method(app: Sanic, access_log):
    app.config.ACCESS_LOG = access_log

    @app.listener("after_server_start")
    async def _request(sanic, loop):
        app.stop()

    app.run(port=1340, access_log=access_log, single_process=True)
    assert app.config.ACCESS_LOG is access_log

def test_stop_method_without_running(app: Sanic):
    with pytest.raises(SanicException):
        app.stop()