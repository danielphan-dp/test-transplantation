import logging
import multiprocessing
import random
import signal
import sys
import pytest
from sanic_testing.testing import HOST
from sanic import Blueprint
from sanic.compat import use_context
from sanic import Sanic

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_method(app: Sanic):
    app.stop()
    assert app.is_stopped is True

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_multiple_times(app: Sanic):
    app.stop()
    app.stop()
    assert app.is_stopped is True

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_with_active_requests(app: Sanic):
    @app.route("/")
    async def test_route(request):
        return "Hello, World!"

    app.run(HOST, 8000, debug=True)
    app.stop()
    assert app.is_stopped is True

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_stop_with_blueprint(app: Sanic):
    bp = Blueprint("test_blueprint")
    
    @bp.route("/bp")
    async def bp_route(request):
        return "Blueprint Route"

    app.blueprint(bp)
    app.run(HOST, 8001, debug=True)
    app.stop()
    assert app.is_stopped is True