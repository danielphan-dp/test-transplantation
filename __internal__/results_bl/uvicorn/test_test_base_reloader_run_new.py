import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn import run

def test_base_reloader_run_no_sockets(tmp_path):
    calls = []
    step = 0

    class CustomReload(BaseReload):
        def startup(self):
            calls.append("startup")

        def restart(self):
            calls.append("restart")

        def shutdown(self):
            calls.append("shutdown")

        def should_restart(self):
            nonlocal step
            step += 1
            if step == 1:
                return None
            elif step == 2:
                return [tmp_path / "foobar.py"]
            else:
                raise StopIteration()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=[])
    reloader.run()

    assert calls == ["startup", "restart", "shutdown"]

def test_base_reloader_run_with_invalid_sockets(tmp_path):
    calls = []
    step = 0

    class CustomReload(BaseReload):
        def startup(self):
            calls.append("startup")

        def restart(self):
            calls.append("restart")

        def shutdown(self):
            calls.append("shutdown")

        def should_restart(self):
            nonlocal step
            step += 1
            if step == 1:
                return None
            elif step == 2:
                return [tmp_path / "invalid.py"]
            else:
                raise StopIteration()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=["invalid_socket"])
    
    with pytest.raises(Exception):
        reloader.run()

def test_base_reloader_run_multiple_restarts(tmp_path):
    calls = []
    step = 0

    class CustomReload(BaseReload):
        def startup(self):
            calls.append("startup")

        def restart(self):
            calls.append("restart")

        def shutdown(self):
            calls.append("shutdown")

        def should_restart(self):
            nonlocal step
            step += 1
            if step < 3:
                return [tmp_path / f"file{step}.py"]
            else:
                raise StopIteration()

    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config, target=run, sockets=[])
    reloader.run()

    assert calls == ["startup", "restart", "restart", "shutdown"]