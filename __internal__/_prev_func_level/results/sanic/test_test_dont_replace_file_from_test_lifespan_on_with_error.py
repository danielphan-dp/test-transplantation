import pytest
from sanic import Sanic

def test_app_stop():
    app = Sanic(name="test_app")

    @app.after_server_start
    def after_start(app: Sanic):
        app.stop()

    app.run(single_process=True)

    assert not app.is_running

def test_app_stop_multiple_times():
    app = Sanic(name="test_app_multiple")

    @app.after_server_start
    def after_start(app: Sanic):
        app.stop()
        app.stop()  # Calling stop multiple times

    app.run(single_process=True)

    assert not app.is_running

def test_app_stop_with_error():
    app = Sanic(name="test_app_error")

    @app.after_server_start
    def after_start(app: Sanic):
        raise RuntimeError("Error during stop")

    with pytest.raises(RuntimeError, match="Error during stop"):
        app.run(single_process=True)

    assert app.is_running  # Ensure app is still running after error

def test_app_stop_no_running_instance():
    app = Sanic(name="test_app_no_instance")

    with pytest.raises(RuntimeError, match="Cannot stop an app that is not running"):
        app.stop()  # Attempting to stop without running

    assert not app.is_running  # Ensure app is not running