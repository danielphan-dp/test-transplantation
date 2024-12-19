import logging
import sys
import pytest
from asyncio import Event
from pathlib import Path
from sanic import Sanic
from sanic.compat import UVLOOP_INSTALLED
from sanic.http.constants import HTTP

@pytest.mark.parametrize('version', (3, HTTP.VERSION_3))
@pytest.mark.skipif(sys.version_info < (3, 8) and (not UVLOOP_INSTALLED), reason='In 3.7 w/o uvloop the port is not always released')
def test_server_stops_correctly(app: Sanic, version, caplog):
    ev = Event()

    @app.after_server_start
    def shutdown(*_):
        ev.set()
        app.stop()

    app.run(
        version=version,
        ssl={
            "cert": Path("localhost_dir/fullchain.pem"),
            "key": Path("localhost_dir/privkey.pem"),
        },
        single_process=True,
    )

    assert ev.is_set()
    assert (
        "sanic.root",
        logging.INFO,
        "server: sanic, HTTP/3",
    ) in caplog.record_tuples

def test_server_stop_without_start(app: Sanic, caplog):
    with caplog.at_level(logging.INFO):
        app.stop()

    assert (
        "sanic.root",
        logging.WARNING,
        "Attempted to stop the server without starting it.",
    ) in caplog.record_tuples

def test_server_stop_multiple_calls(app: Sanic, version, caplog):
    ev = Event()

    @app.after_server_start
    def shutdown(*_):
        ev.set()
        app.stop()
        app.stop()  # Call stop again to test multiple calls

    with caplog.at_level(logging.INFO):
        app.run(
            version=version,
            ssl={
                "cert": Path("localhost_dir/fullchain.pem"),
                "key": Path("localhost_dir/privkey.pem"),
            },
            single_process=True,
        )

    assert ev.is_set()
    assert (
        "sanic.root",
        logging.INFO,
        "server: sanic, HTTP/3",
    ) in caplog.record_tuples
    assert (
        "sanic.root",
        logging.WARNING,
        "Server is already stopped.",
    ) in caplog.record_tuples