import pytest
from unittest import mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

def test_shutdown_method_calls_shutdown():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=[])

    reloader.shutdown()

    assert 'shutdown' in calls

def test_shutdown_with_no_active_connections():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=[])

    reloader.shutdown()

    assert calls == ['shutdown']

def test_shutdown_multiple_calls():
    calls = []

    class CustomReload(BaseReload):
        def shutdown(self):
            calls.append('shutdown')
            super().shutdown()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=[])

    reloader.shutdown()
    reloader.shutdown()

    assert calls == ['shutdown', 'shutdown']