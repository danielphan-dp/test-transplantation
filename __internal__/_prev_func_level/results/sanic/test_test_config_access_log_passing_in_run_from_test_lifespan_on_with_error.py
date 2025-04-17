import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.mark.parametrize('access_log', (True, False))
def test_app_stop(app: Sanic, access_log):
    assert app.config.ACCESS_LOG is False

    @app.listener("after_server_start")
    async def _stop_app(sanic, loop):
        app.stop()

    app.run(port=1340, access_log=access_log, single_process=True)
    assert app.config.ACCESS_LOG is access_log

    with pytest.raises(SanicException):
        app.stop()  # Ensure that calling stop again raises an exception

    # Additional test to ensure the app is indeed stopped
    assert not app.is_running  # Assuming is_running is a property that indicates if the app is running