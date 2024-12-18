import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_with_no_changes(self, touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"

    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file)

        # Simulate no changes
        assert self._reload_tester(touch_soon, reloader, app_file) is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [BaseReload])
def test_should_not_reload_when_no_files_touched(self, touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file = app_dir / "src" / "main.py"

    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        # Initial touch to simulate file existence
        app_file.touch()
        assert self._reload_tester(touch_soon, reloader, app_file)

        # No touch action, should not trigger reload
        assert self._reload_tester(touch_soon, reloader, app_file) is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_multiple_files(self, touch_soon) -> None:
    app_dir = self.reload_path / "app"
    app_file1 = app_dir / "src" / "main.py"
    app_file2 = app_dir / "src" / "utils.py"

    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_dirs=[str(app_dir)],
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, app_file1)
        assert self._reload_tester(touch_soon, reloader, app_file2)

        # Touch both files to trigger reload
        app_file1.touch()
        app_file2.touch()
        assert self._reload_tester(touch_soon, reloader, app_file1)
        assert self._reload_tester(touch_soon, reloader, app_file2)

        reloader.shutdown()