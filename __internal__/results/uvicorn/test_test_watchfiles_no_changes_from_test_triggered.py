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
    sub_dir = Path("app/sub")

    with as_cwd(Path("reload_path")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[str(sub_dir)],
        )
        reloader = _setup_reloader(config)

        assert isinstance(reloader, reloader_class)
        assert config.should_reload

        reloader.shutdown()

def test_reloader_should_restart_on_file_change() -> None:
    sub_dir = Path("app/sub")
    mock_touch = Mock()

    with as_cwd(Path("reload_path")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[str(sub_dir)],
        )
        reloader = _setup_reloader(config)

        reloader.restart()
        mock_touch(sub_dir / "file.py")

        assert reloader.should_restart() is not None

        reloader.shutdown()

def test_reloader_should_not_restart_when_no_changes() -> None:
    sub_dir = Path("app/sub")

    with as_cwd(Path("reload_path")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[str(sub_dir)],
        )
        reloader = _setup_reloader(config)

        assert reloader.should_restart() is None

        reloader.shutdown()