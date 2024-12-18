import pytest
from unittest.mock import Mock
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_not_reload_when_no_changes(touch_soon) -> None:
    app_dir = Path("app")
    app_file = app_dir / "src" / "main.py"
    
    with as_cwd(app_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        # Simulate no changes
        assert self._reload_tester(touch_soon, reloader, app_file) is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_when_file_is_touched(touch_soon) -> None:
    app_dir = Path("app")
    app_file = app_dir / "src" / "main.py"

    with as_cwd(app_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        # Touch the file to simulate a change
        app_file.touch()
        assert self._reload_tester(touch_soon, reloader, app_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_multiple_files(touch_soon) -> None:
    app_dir = Path("app")
    app_file_1 = app_dir / "src" / "main.py"
    app_file_2 = app_dir / "src" / "utils.py"

    with as_cwd(app_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        # Touch both files to simulate changes
        app_file_1.touch()
        app_file_2.touch()
        assert self._reload_tester(touch_soon, reloader, app_file_1)
        assert self._reload_tester(touch_soon, reloader, app_file_2)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_not_reload_when_excluded(touch_soon) -> None:
    app_dir = Path("app")
    excluded_file = app_dir / "excluded.py"
    included_file = app_dir / "included.py"

    with as_cwd(app_dir):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[str(excluded_file)],
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        # Touch the included file
        included_file.touch()
        assert self._reload_tester(touch_soon, reloader, included_file)

        # Ensure excluded file does not trigger a reload
        excluded_file.touch()
        assert self._reload_tester(touch_soon, reloader, excluded_file) is None

        reloader.shutdown()