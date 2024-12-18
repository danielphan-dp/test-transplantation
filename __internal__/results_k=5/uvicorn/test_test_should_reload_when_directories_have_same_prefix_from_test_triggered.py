import pytest
from unittest.mock import Mock
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_should_reload_with_multiple_files(self, touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"
    another_app_file = app_dir / "src" / "another.py"
    
    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file, another_app_file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_should_not_reload_when_no_changes(self, touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"
    
    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file) is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_should_reload_when_file_touched(self, touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"
    
    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        app_file.touch()
        sleep(0.1)  # Allow time for the reloader to detect the change
        assert self._reload_tester(touch_soon, reloader, app_file)

        reloader.shutdown()