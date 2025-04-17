import pytest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
def test_reloader_initialization_with_different_classes(reloader_class) -> None:
    sub_dir = "app/sub"

    with as_cwd("path/to/reload"):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[sub_dir],
        )
        reloader = _setup_reloader(config)

        assert isinstance(reloader, reloader_class)
        assert config.should_reload

        reloader.shutdown()

def test_reloader_should_startup_and_shutdown() -> None:
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = _setup_reloader(config)

    assert reloader is not None
    reloader.startup()
    assert reloader.should_exit.is_set() is False

    reloader.shutdown()
    assert reloader.should_exit.is_set() is True

def test_reloader_should_not_restart_when_no_changes() -> None:
    sub_dir = "app/sub"

    with as_cwd("path/to/reload"):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[sub_dir],
        )
        reloader = _setup_reloader(config)

        assert reloader.should_restart() is None

        reloader.shutdown()

def test_reloader_should_handle_exceptions_during_startup() -> None:
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = _setup_reloader(config)

    with pytest.raises(Exception):
        reloader.startup()  # Simulate an exception during startup

    reloader.shutdown()