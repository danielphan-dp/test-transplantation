import logging
import sys
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException
from asyncio import Event

@pytest.mark.parametrize('version', (3, HTTP.VERSION_3))
@pytest.mark.skipif(sys.version_info < (3, 8), reason='Requires Python 3.8 or higher')
def test_app_stop(app: Sanic, version, caplog):
    ev = Event()

    @app.after_server_stop
    def on_stop(*_):
        ev.set()

    app.stop()

    with caplog.at_level(logging.INFO):
        app.run(
            version=version,
            ssl={
                "cert": localhost_dir / "fullchain.pem",
                "key": localhost_dir / "privkey.pem",
            },
            single_process=True,
        )

    assert ev.is_set()
    assert (
        "sanic.root",
        logging.INFO,
        "server stopped",
    ) in caplog.record_tuples

def test_app_stop_with_exception(app: Sanic, caplog):
    app.stop()
    with pytest.raises(SanicException):
        app.stop()  # Attempting to stop an already stopped app should raise an exception

    assert "Application has already been stopped" in caplog.text