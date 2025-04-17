import pytest
from sanic import Sanic
from sanic_ext import Extend

@pytest.fixture
def app():
    app = Sanic("TestApp")
    Extend(app)
    return app

def test_app_stops_correctly(app):
    @app.before_server_start
    async def start():
        pass

    @app.before_server_stop
    async def stop():
        app.stop()

    app.run(single_process=True)
    assert not app.is_running

def test_app_stop_called_twice(app):
    @app.before_server_start
    async def start():
        pass

    @app.before_server_stop
    async def stop():
        app.stop()
        app.stop()  # Calling stop again

    app.run(single_process=True)
    assert not app.is_running

def test_app_stop_with_error(app):
    @app.before_server_start
    async def start():
        raise RuntimeError("Startup error")

    @app.before_server_stop
    async def stop():
        app.stop()

    with pytest.raises(RuntimeError, match="Startup error"):
        app.run(single_process=True)