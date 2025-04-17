import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reloader_should_initialize(self, touch_soon) -> None:
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert reloader is not None
        reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reload_with_no_files(self, touch_soon) -> None:
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert not self._reload_tester(touch_soon, reloader)

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reload_with_nonexistent_file(self, touch_soon) -> None:
        nonexistent_file = self.reload_path / "nonexistent.py"
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert not self._reload_tester(touch_soon, reloader, nonexistent_file)

    @pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
    def test_reload_with_multiple_files(self, touch_soon) -> None:
        file1 = self.reload_path / "file1.py"
        file2 = self.reload_path / "file2.py"
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader, file1, file2)

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    def _reload_tester(self, touch_soon, reloader: BaseReload, *files: Path) -> list[Path] | None:
        reloader.restart()
        for file in files:
            file.touch()
        return next(reloader)