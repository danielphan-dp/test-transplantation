import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from pathlib import Path

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path, reloader_class: type[BaseReload] | None):
        if reloader_class is None:
            pytest.skip("Needed dependency not installed")
        self.reload_path = reload_directory_structure
        self.reloader_class = reloader_class

    @pytest.mark.parametrize("reloader_class, expected_should_reload", [
        (StatReload, True),
        (WatchFilesReload, True),
        (WatchGodReload, True)
    ])
    def test_reloader_should_initialize_with_various_classes(self, reloader_class, expected_should_reload):
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            assert config.should_reload == expected_should_reload
            reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload, WatchGodReload])
    def test_reload_when_python_file_is_changed(self, reloader_class, touch_soon: Callable[[Path], None]):
        file = self.reload_path / "main.py"

        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)

            # Simulate file change
            touch_soon(file)
            assert bool(self._reload_tester(touch_soon, reloader, file))

            reloader.shutdown()

    @pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload, WatchGodReload])
    def test_reloader_should_not_start_if_should_reload_is_false(self, reloader_class):
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=False)
            reloader = self._setup_reloader(config)
            assert not config.should_reload
            reloader.shutdown()