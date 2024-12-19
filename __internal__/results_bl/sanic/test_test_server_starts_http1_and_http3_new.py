import logging
import sys
import pytest
from sanic import Sanic

@pytest.mark.skipif(sys.version_info < (3, 8) and (not UVLOOP_INSTALLED), reason='In 3.7 w/o uvloop the port is not always released')
def test_stop_method_stops_app(app: Sanic):
    app_started = False

    @app.after_server_start
    def start_server(*_):
        nonlocal app_started
        app_started = True

    app.prepare(
        version=3,
        ssl={
            "cert": localhost_dir / "fullchain.pem",
            "key": localhost_dir / "privkey.pem",
        },
    )
    
    assert not app_started
    app.stop()
    assert not app_started

def test_stop_method_when_not_running(app: Sanic):
    with pytest.raises(RuntimeError):
        app.stop()