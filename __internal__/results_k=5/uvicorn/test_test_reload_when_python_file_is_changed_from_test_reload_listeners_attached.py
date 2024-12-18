import pytest
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

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0  # save time
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
    def test_reloader_should_initialize(self) -> None:
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
    def test_reload_when_no_file_changes(self, touch_soon) -> None:
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        file = self.reload_path / "main.py"

        with as_cwd(self.reload_path):
            changes = self._reload_tester(touch_soon, reloader, file)
            assert changes is None  # No changes should be detected

            reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
    def test_reload_when_multiple_files_changed(self, touch_soon) -> None:
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        files = [self.reload_path / f"file_{i}.py" for i in range(3)]

        with as_cwd(self.reload_path):
            changes = self._reload_tester(touch_soon, reloader, *files)
            assert set(changes) == set(files)  # All files should be detected

            reloader.shutdown()