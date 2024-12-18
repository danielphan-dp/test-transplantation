import pytest
from unittest.mock import Mock
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
def test_reloader_initialization_with_different_classes(reloader_class) -> None:
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert isinstance(reloader, reloader_class)
        assert config.should_reload

        reloader.shutdown()

def test_reloader_should_not_start_if_not_configured() -> None:
    config = Config(app="tests.test_config:asgi_app", reload=False)
    reloader = self._setup_reloader(config)

    assert not config.should_reload
    with pytest.raises(Exception):
        reloader.startup()

def test_reloader_should_restart_on_file_change(touch_soon: Callable[[Path], None]) -> None:
    file = self.reload_path / "main.py"
    with as_cwd(self.reload_path):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        reloader.restart()
        touch_soon(file)

        assert reloader.should_restart() is not None

        reloader.shutdown()