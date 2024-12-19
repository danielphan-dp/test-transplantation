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
    
    @app.after_server_start
    def after_start(*_):
        app.stop()
        ev.set()

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
        "server: sanic, HTTP/3",
    ) in caplog.record_tuples

def test_app_stop_no_event(app: Sanic):
    with pytest.raises(SanicException):
        app.stop()