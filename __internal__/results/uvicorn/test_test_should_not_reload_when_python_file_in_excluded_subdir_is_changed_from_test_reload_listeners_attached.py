import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils import as_cwd

@pytest.mark.parametrize('reloader_class', [WatchFilesReload, WatchGodReload])
def test_should_reload_when_python_file_is_changed(self, touch_soon) -> None:
    file_to_change = self.reload_path / "main.py"

    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
        )
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file_to_change)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload, WatchGodReload])
def test_should_not_reload_when_config_is_invalid(self, touch_soon) -> None:
    invalid_file = self.reload_path / "invalid.py"

    with as_cwd(self.reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[str(invalid_file)],
        )
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, invalid_file)

        reloader.shutdown()