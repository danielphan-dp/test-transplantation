import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_reloader_shutdown_calls_shutdown_method():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=[])

    reloader.shutdown()

    assert "shutdown" in calls

def test_reloader_shutdown_with_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=[])

    reloader.shutdown()

    assert calls == ["shutdown"]

def test_reloader_shutdown_with_active_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=[])

    # Simulate active connections
    reloader.server_state.connections = ["connection1", "connection2"]

    reloader.shutdown()

    assert calls == ["shutdown"]
    assert len(reloader.server_state.connections) == 0  # Ensure connections are cleared

def test_reloader_shutdown_does_not_fail_on_empty_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=lambda: None, sockets=[])

    # Ensure no connections are present
    reloader.server_state.connections = []

    reloader.shutdown()

    assert calls == ["shutdown"]