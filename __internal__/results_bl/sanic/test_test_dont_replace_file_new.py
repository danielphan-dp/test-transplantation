import logging
import os
import sys
import asyncio
import pytest
from pathlib import Path
from sanic import Sanic
from sanic.exceptions import SanicException

SOCKPATH = Path("/tmp/test_socket")

@pytest.fixture
def app():
    app = Sanic(name="test")
    yield app

def test_stop_app(app):
    @app.after_server_start
    def stop_app(app: Sanic):
        app.stop()

    app.run(unix=SOCKPATH, single_process=True)

def test_stop_app_not_running(app):
    with pytest.raises(SanicException):
        app.stop()

def test_stop_app_multiple_calls(app):
    @app.after_server_start
    def stop_app(app: Sanic):
        app.stop()
        app.stop()  # Calling stop again to test idempotency

    app.run(unix=SOCKPATH, single_process=True)

def test_stop_app_with_no_running_server(app):
    app.stop()  # Test stopping without running the server should not raise an error

def test_stop_app_with_invalid_app(app):
    with pytest.raises(TypeError):
        stop(None)  # Passing None to stop should raise a TypeError