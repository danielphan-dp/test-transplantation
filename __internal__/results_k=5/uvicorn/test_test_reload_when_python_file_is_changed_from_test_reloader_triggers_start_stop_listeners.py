import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_when_multiple_files_are_changed(self, touch_soon) -> None:
    files = [self.reload_path / f"file_{i}.py" for i in range(3)]

    for file in files:
        file.touch()

    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        changes = self._reload_tester(touch_soon, reloader, *files)
        assert set(changes) == set(files)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [BaseReload])
def test_reload_when_no_files_are_changed(self, touch_soon) -> None:
    file = self.reload_path / "unchanged_file.py"
    file.touch()

    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        changes = self._reload_tester(touch_soon, reloader, file)
        assert changes is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_reload_with_invalid_file(self, touch_soon) -> None:
    invalid_file = self.reload_path / "invalid_file.py"

    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        changes = self._reload_tester(touch_soon, reloader, invalid_file)
        assert changes is None

        reloader.shutdown()