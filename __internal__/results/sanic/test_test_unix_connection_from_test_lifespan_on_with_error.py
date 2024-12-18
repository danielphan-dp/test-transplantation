import os
import pytest
from sanic import Sanic
from sanic.response import text

def test_app_stop():
    app = Sanic(name="test_app_stop")

    @app.get("/")
    async def handler(request):
        return text("Server is running")

    @app.after_server_start
    async def after_start(app):
        assert app.is_running
        app.stop()
        assert not app.is_running

    app.run(host="localhost", port=8000, single_process=True)

def test_app_stop_when_not_running():
    app = Sanic(name="test_app_stop_not_running")

    @app.get("/")
    async def handler(request):
        return text("Server is running")

    @app.after_server_start
    async def after_start(app):
        app.stop()
        with pytest.raises(RuntimeError):
            app.stop()  # Attempting to stop again should raise an error

    app.run(host="localhost", port=8001, single_process=True)