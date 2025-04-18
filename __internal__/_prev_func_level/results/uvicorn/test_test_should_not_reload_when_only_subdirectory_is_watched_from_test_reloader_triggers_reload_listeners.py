import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    def _reload_tester(self, touch_soon: Callable[[Path], None], reloader: BaseReload, *files: Path) -> list[Path] | None:
        reloader.restart()
        if WatchFilesReload is not None and isinstance(reloader, WatchFilesReload):
            touch_soon(*files)
        else:
            assert not next(reloader)
            sleep(0.1)
            for file in files:
                file.touch()
        return next(reloader)

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, pytest.param(WatchFilesReload, marks=skip_if_m1)])
    def test_should_reload_when_file_in_root_directory_is_changed(self, touch_soon: Callable[[Path], None]) -> None:
        root_file = self.reload_path / "main.py"
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_dirs=[str(self.reload_path)])
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, root_file)

        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, pytest.param(WatchFilesReload, marks=skip_if_m1)])
    def test_should_not_reload_when_no_files_are_changed(self, touch_soon: Callable[[Path], None]) -> None:
        app_dir = self.reload_path / "app"
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_dirs=[str(app_dir)])
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, app_dir / "non_existent_file.py")

        reloader.shutdown()