import logging
import pytest
from sanic import Sanic

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Requires Python 3.8 or higher')
def test_app_stop(app: Sanic, caplog):
    @app.after_server_start
    def after_start(*_):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.stop()

    assert (
        "sanic.root",
        logging.INFO,
        "server: sanic, stopped",
    ) in caplog.record_tuples

def test_app_stop_no_running_server(app: Sanic, caplog):
    with caplog.at_level(logging.WARNING):
        app.stop()

    assert (
        "sanic.root",
        logging.WARNING,
        "server: sanic, already stopped",
    ) in caplog.record_tuples

def test_app_stop_with_tasks(app: Sanic, caplog):
    app.shutdown_tasks = Mock()

    @app.after_server_start
    def after_start(*_):
        app.stop()

    app.stop()

    app.shutdown_tasks.assert_called_once()