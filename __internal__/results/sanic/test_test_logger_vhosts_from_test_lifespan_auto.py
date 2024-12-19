import logging
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

def test_app_stop():
    app = Sanic(name="test_app_stop")

    @app.after_server_start
    def after_start(*args):
        app.stop()

    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    with pytest.raises(SanicException):
        app.stop()

    app.run(host="127.0.0.1", port=42102, single_process=True)

    assert app.is_running is False

def test_app_stop_multiple_calls():
    app = Sanic(name="test_app_stop_multiple_calls")

    @app.after_server_start
    def after_start(*args):
        app.stop()

    app.run(host="127.0.0.1", port=42102, single_process=True)

    app.stop()
    assert app.is_running is False

def test_app_stop_with_tasks():
    app = Sanic(name="test_app_stop_with_tasks")

    @app.after_server_start
    async def after_start(*args):
        await app.stop()

    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    app.run(host="127.0.0.1", port=42102, single_process=True)

    assert app.is_running is False