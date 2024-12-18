import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_reloader_shutdown_calls_shutdown_method():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()

    assert "shutdown" in calls

def test_reloader_shutdown_with_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=None)

    reloader.shutdown()

    assert "shutdown" in calls

def test_reloader_shutdown_multiple_calls():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()

    assert calls.count("shutdown") == 2

def test_reloader_shutdown_with_active_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    # Simulate active connections
    reloader.server_state.connections = ["connection1", "connection2"]

    reloader.shutdown()

    assert "shutdown" in calls
    assert len(reloader.server_state.connections) == 0  # Ensure connections are cleared after shutdown

def test_reloader_shutdown_logs_shutdown_message(caplog):
    class CustomReload(BaseReload):
        def shutdown(self):
            logger.info("Shutting down")

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    with caplog.at_level(logging.INFO):
        reloader.shutdown()

    assert "Shutting down" in caplog.text