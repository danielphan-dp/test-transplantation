import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class, result', [(StatReload, False), (WatchFilesReload, True)])
def test_reload_when_no_files_changed(self, reloader_class, result, touch_soon) -> None:
    file = self.reload_path / "app" / "js" / "main.js"

    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = self._setup_reloader(config)

        assert bool(self._reload_tester(touch_soon, reloader, file)) == result

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class, result', [(StatReload, False), (WatchFilesReload, True)])
def test_reload_with_multiple_files(self, reloader_class, result, touch_soon) -> None:
    files = [self.reload_path / "app" / "js" / f"file_{i}.js" for i in range(3)]

    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = self._setup_reloader(config)

        assert bool(self._reload_tester(touch_soon, reloader, *files)) == result

        reloader.shutdown()

def test_reload_with_invalid_file(self) -> None:
    invalid_file = Path("invalid_path.js")

    with pytest.raises(FileNotFoundError):
        self._reload_tester(lambda *args: None, WatchFilesReload(), invalid_file)

def test_reload_with_empty_file_list(self) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = self._setup_reloader(config)

        assert self._reload_tester(lambda *args: None, reloader) is None

        reloader.shutdown()