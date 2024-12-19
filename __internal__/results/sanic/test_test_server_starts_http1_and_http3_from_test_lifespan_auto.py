import logging
import sys
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Requires Python 3.8 or higher')
def test_app_stop_method(app: Sanic, caplog):
    @app.listener('after_server_start')
    def after_start(*_):
        app.stop()

    with caplog.at_level(logging.INFO):
        app.run()

    assert ('sanic.root', logging.INFO, 'server stopped') in caplog.record_tuples

def test_app_stop_without_start(app: Sanic):
    with pytest.raises(SanicException, match="Cannot stop a server that is not running"):
        app.stop()