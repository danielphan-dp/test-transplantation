import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from time import sleep

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, pytest.param(WatchFilesReload, marks=pytest.mark.skip)])
def test_should_reload_when_file_is_touched(self, touch_soon, reloader_class) -> None:
    app_dir = self.reload_path / "app"
    app_dir_file = self.reload_path / "app" / "src" / "main.py"
    
    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    # Touch the file to trigger a reload
    app_dir_file.touch()
    assert self._reload_tester(touch_soon, reloader, app_dir_file)

    reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, pytest.param(WatchFilesReload, marks=pytest.mark.skip)])
def test_should_not_reload_when_file_is_not_touched(self, touch_soon, reloader_class) -> None:
    app_dir = self.reload_path / "app"
    app_dir_file = self.reload_path / "app" / "src" / "main.py"
    root_file = self.reload_path / "main.py"

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    assert not self._reload_tester(touch_soon, reloader, root_file)
    assert not self._reload_tester(touch_soon, reloader, app_dir / "~ignored")

    reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, pytest.param(WatchFilesReload, marks=pytest.mark.skip)])
def test_should_reload_multiple_files(self, touch_soon, reloader_class) -> None:
    app_dir = self.reload_path / "app"
    app_dir_file1 = self.reload_path / "app" / "src" / "main.py"
    app_dir_file2 = self.reload_path / "app" / "src" / "utils.py"

    config = Config(
        app="tests.test_config:asgi_app",
        reload=True,
        reload_dirs=[str(app_dir)],
    )
    reloader = self._setup_reloader(config)

    app_dir_file1.touch()
    app_dir_file2.touch()
    assert self._reload_tester(touch_soon, reloader, app_dir_file1, app_dir_file2)

    reloader.shutdown()