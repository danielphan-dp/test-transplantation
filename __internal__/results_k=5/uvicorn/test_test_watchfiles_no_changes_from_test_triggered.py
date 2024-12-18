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
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = _setup_reloader(config)

    assert isinstance(reloader, reloader_class)
    assert config.should_reload
    reloader.shutdown()

def test_reloader_should_not_restart_when_no_changes() -> None:
    sub_dir = Path("app/sub")
    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_excludes=[str(sub_dir)])
        reloader = _setup_reloader(config)

        reloader.watcher = Mock()
        reloader.should_restart = Mock(return_value=None)

        assert reloader.should_restart() is None
        reloader.shutdown()

def test_reloader_should_restart_on_file_change() -> None:
    file_to_change = Path("app/main.py")
    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        reloader.should_restart = Mock(return_value=[file_to_change])
        reloader.restart()

        assert reloader.should_restart() == [file_to_change]
        reloader.shutdown()

def test_reloader_with_invalid_config() -> None:
    config = Config(app="tests.test_config:asgi_app", reload=False)
    with pytest.raises(ValueError):
        _setup_reloader(config)