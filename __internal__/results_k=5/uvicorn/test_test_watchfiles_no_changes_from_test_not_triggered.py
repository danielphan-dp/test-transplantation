import pytest
from unittest.mock import Mock
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
def test_reloader_initialization(reloader_class) -> None:
    reload_path = Path("/path/to/reload")
    
    with as_cwd(reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        assert isinstance(reloader, reloader_class)
        assert config.should_reload

        reloader.shutdown()

def test_reloader_should_not_restart_when_no_changes() -> None:
    reload_path = Path("/path/to/reload")
    sub_dir = reload_path / "app" / "sub"

    with as_cwd(reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_excludes=[str(sub_dir)])
        reloader = _setup_reloader(config)

        assert isinstance(reloader, WatchFilesReload)
        assert reloader.should_restart() is None

        reloader.shutdown()

def test_reloader_should_trigger_on_file_change(touch_soon) -> None:
    reload_path = Path("/path/to/reload")
    file_to_change = reload_path / "main.py"

    with as_cwd(reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        reloader.restart()
        touch_soon(file_to_change)

        assert reloader.should_restart() is not None

        reloader.shutdown()

def test_reloader_should_exit_on_signal() -> None:
    reload_path = Path("/path/to/reload")
    
    with as_cwd(reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        reloader.signal_handler(signal.SIGTERM, None)
        assert reloader.should_exit.is_set()

        reloader.shutdown()