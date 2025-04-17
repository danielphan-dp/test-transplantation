import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn import run

def test_run_with_empty_sockets():
    calls = []

    class CustomReload(BaseReload):
        def startup(self):
            calls.append("startup")

        def restart(self):
            calls.append("restart")

        def shutdown(self):
            calls.append("shutdown")

        def should_restart(self):
            return None

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=[])
    reloader.run()

    assert calls == ["startup", "shutdown"]

def test_run_with_invalid_sockets():
    calls = []

    class CustomReload(BaseReload):
        def startup(self):
            calls.append("startup")

        def restart(self):
            calls.append("restart")

        def shutdown(self):
            calls.append("shutdown")

        def should_restart(self):
            return ["invalid_socket"]

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=["invalid_socket"])
    
    with pytest.raises(Exception):
        reloader.run()

    assert calls == ["startup", "shutdown"]

def test_run_with_multiple_sockets(tmp_path):
    calls = []
    socket1 = tmp_path / "socket1.sock"
    socket2 = tmp_path / "socket2.sock"

    class CustomReload(BaseReload):
        def startup(self):
            calls.append("startup")

        def restart(self):
            calls.append("restart")

        def shutdown(self):
            calls.append("shutdown")

        def should_restart(self):
            return [socket1, socket2]

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=[socket1, socket2])
    reloader.run()

    assert calls == ["startup", "restart", "shutdown"]