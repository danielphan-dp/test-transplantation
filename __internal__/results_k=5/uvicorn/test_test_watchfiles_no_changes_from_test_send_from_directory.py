import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

calls = []

class CustomReload(BaseReload):
    def shutdown(self):
        calls.append("shutdown")
        super().shutdown()

def test_base_reloader_shutdown():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])
    
    reloader.shutdown()
    
    assert "shutdown" in calls

def test_base_reloader_shutdown_multiple_calls():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()
    reloader.shutdown()

    assert calls.count("shutdown") == 2

def test_base_reloader_shutdown_no_sockets():
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=None, sockets=[])

    reloader.shutdown()

    assert calls == ["shutdown"]