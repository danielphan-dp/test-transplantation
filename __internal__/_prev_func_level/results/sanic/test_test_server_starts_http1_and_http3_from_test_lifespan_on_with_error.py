import logging
import pytest
from sanic import Sanic

@pytest.mark.skipif(sys.version_info < (3, 8) and (not UVLOOP_INSTALLED), reason='In 3.7 w/o uvloop the port is not always released')
def test_app_stop(app: Sanic, caplog):
    @app.after_server_start
    def after_start(*_):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.stop()

    assert (
        "sanic.root",
        logging.INFO,
        "server stopped",
    ) in caplog.record_tuples

def test_app_stop_no_running_server(app: Sanic, caplog):
    with caplog.at_level(logging.WARNING):
        app.stop()

    assert (
        "sanic.root",
        logging.WARNING,
        "server was not running",
    ) in caplog.record_tuples

def test_app_stop_multiple_calls(app: Sanic, caplog):
    @app.after_server_start
    def after_start(*_):
        app.stop()
        app.stop()  # Calling stop again

    with caplog.at_level(logging.INFO):
        app.stop()

    assert (
        "sanic.root",
        logging.INFO,
        "server stopped",
    ) in caplog.record_tuples
    assert caplog.text.count("server stopped") == 1  # Ensure it only logs once