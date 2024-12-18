import pytest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
def test_reloader_initialization_with_different_classes(reloader_class) -> None:
    with as_cwd("path/to/reload"):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        assert isinstance(reloader, reloader_class)
        assert config.should_reload
        reloader.shutdown()

def test_reloader_should_not_start_if_not_configured() -> None:
    config = Config(app="tests.test_config:asgi_app", reload=False)
    reloader = _setup_reloader(config)

    assert reloader is None

def test_reloader_should_trigger_on_file_change(touch_soon: Callable[[Path], None]) -> None:
    file = "path/to/reload/main.py"
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = _setup_reloader(config)

    touch_soon(file)
    assert reloader.should_restart() is not None

def test_reloader_shutdown_properly() -> None:
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = _setup_reloader(config)

    reloader.shutdown()
    assert reloader.should_exit.is_set()