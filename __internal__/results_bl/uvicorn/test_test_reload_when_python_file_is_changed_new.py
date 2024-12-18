import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_reload_when_no_file_changes(self, touch_soon, reloader_class) -> None:
    file = self.reload_path / "main.py"
    
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        changes = self._reload_tester(touch_soon, reloader, file)
        assert changes is None

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_reload_with_multiple_file_changes(self, touch_soon, reloader_class) -> None:
    file1 = self.reload_path / "main.py"
    file2 = self.reload_path / "utils.py"
    
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        changes = self._reload_tester(touch_soon, reloader, file1, file2)
        assert set(changes) == {file1, file2}

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [StatReload, WatchGodReload, WatchFilesReload])
def test_reload_with_nonexistent_file(self, touch_soon, reloader_class) -> None:
    nonexistent_file = self.reload_path / "nonexistent.py"
    
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        with pytest.raises(FileNotFoundError):
            self._reload_tester(touch_soon, reloader, nonexistent_file)

        reloader.shutdown()