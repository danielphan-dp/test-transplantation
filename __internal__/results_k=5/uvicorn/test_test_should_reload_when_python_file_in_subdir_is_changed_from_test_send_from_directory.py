import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_shutdown_method_calls_shutdown():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()

    assert "shutdown" in calls

def test_shutdown_with_no_sockets():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()

    assert calls == ["shutdown"]

def test_shutdown_with_multiple_calls():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append("shutdown")
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()

    assert calls == ["shutdown", "shutdown"]