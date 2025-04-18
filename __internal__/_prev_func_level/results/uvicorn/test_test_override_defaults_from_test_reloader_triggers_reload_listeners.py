import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

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

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_trigger_on_file_change(self, touch_soon) -> None:
        test_file = self.reload_path / "test_file.txt"
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, test_file)

        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_not_trigger_on_excluded_file_change(self, touch_soon) -> None:
        excluded_file = self.reload_path / "excluded_file.py"
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_excludes=["*.py"])
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, excluded_file)

        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_handle_multiple_file_changes(self, touch_soon) -> None:
        file1 = self.reload_path / "file1.txt"
        file2 = self.reload_path / "file2.txt"
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2)

        reloader.shutdown()