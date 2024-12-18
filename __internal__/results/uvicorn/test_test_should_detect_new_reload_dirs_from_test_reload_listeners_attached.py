import logging
import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

class TestBaseReload:
    @pytest.fixture(autouse=True)
    def setup(self, reload_directory_structure: Path):
        self.reload_path = reload_directory_structure
        self.reloader_class = WatchGodReload

    def _setup_reloader(self, config: Config) -> BaseReload:
        config.reload_delay = 0
        reloader = self.reloader_class(config, target=run, sockets=[])
        assert config.should_reload
        reloader.startup()
        return reloader

    def test_reloader_should_initialize(self):
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True)
            reloader = self._setup_reloader(config)
            reloader.shutdown()

    def test_reloader_should_not_start_without_reload(self):
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=False)
            reloader = self._setup_reloader(config)
            assert not config.should_reload
            reloader.shutdown()

    def test_reloader_should_handle_empty_reload_dirs(self, caplog):
        with as_cwd(self.reload_path):
            config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=[])
            reloader = self._setup_reloader(config)
            assert caplog.records[-1].message == "No directories to watch for reload."
            reloader.shutdown()

    def test_reloader_should_detect_multiple_reload_dirs(self, touch_soon, caplog, tmp_path: Path):
        app_dir = tmp_path / "app"
        app_file = app_dir / "file.py"
        app_dir.mkdir()
        app_second_dir = tmp_path / "app_second"
        app_second_file = app_second_dir / "file.py"

        with as_cwd(tmp_path):
            config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
            reloader = self._setup_reloader(config)
            assert self._reload_tester(touch_soon, reloader, app_file)

            app_second_dir.mkdir()
            assert self._reload_tester(touch_soon, reloader, app_second_file)
            assert caplog.records[-2].levelno == logging.INFO
            assert (
                caplog.records[-1].message == "WatchGodReload detected a new reload "
                f"dir '{app_second_dir.name}' in '{tmp_path}'; Adding to watch list."
            )

            reloader.shutdown()