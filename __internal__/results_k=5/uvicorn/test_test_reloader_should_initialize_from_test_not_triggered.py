import pytest
from unittest.mock import Mock
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:  # pragma: no cover
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
    def test_reloader_should_initialize_with_different_classes(self, reloader_class) -> None:
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            assert isinstance(reloader, reloader_class)
            reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
    def test_reloader_should_not_start_if_not_configured(self, reloader_class) -> None:
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=False)
            reloader = self._setup_reloader(config)
            assert not config.should_reload
            with pytest.raises(Exception):
                reloader.startup()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
    def test_reloader_should_handle_startup_failure(self, reloader_class) -> None:
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            reloader.startup()
            # Simulate a failure in startup
            reloader.should_exit.set()
            with pytest.raises(SystemExit):
                reloader.run()

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    def test_reloader_should_trigger_on_file_change(self, touch_soon: Callable[[Path], None]) -> None:
        file = self.reload_path / "main.py"
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            reloader.restart()
            touch_soon(file)
            assert reloader.should_restart() is not None
            reloader.shutdown()