import os
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

SOCKPATH = "/tmp/test.sock"

@pytest.fixture
def app():
    app = Sanic(name="test")
    yield app

def test_stop_method_stops_app(app):
    @app.after_server_start
    async def start_handler(app: Sanic):
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert app.is_stopped

def test_stop_method_when_not_running(app):
    with pytest.raises(SanicException):
        app.stop()

def test_stop_method_multiple_calls(app):
    @app.after_server_start
    async def start_handler(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert app.is_stopped

def test_stop_method_with_active_requests(app):
    @app.route("/")
    async def test_route(request):
        return "Hello, World!"

    @app.after_server_start
    async def start_handler(app: Sanic):
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert app.is_stopped

def test_stop_method_with_unlinked_socket(app):
    @app.after_server_start
    async def start_handler(app: Sanic):
        os.unlink(SOCKPATH)
        app.stop()

    app.run(host="myhost.invalid", unix=SOCKPATH, single_process=True)
    assert app.is_stopped