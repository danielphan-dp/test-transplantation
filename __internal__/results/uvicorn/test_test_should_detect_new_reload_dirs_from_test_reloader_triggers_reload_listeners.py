import logging
import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchGodReload])
def test_reloader_should_startup_and_shutdown(touch_soon, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    config = Config(app="tests.test_config:asgi_app", reload=True)
    
    with as_cwd(tmp_path):
        reloader = self._setup_reloader(config)
        assert config.should_reload
        reloader.startup()
        
        assert caplog.records[-1].levelno == logging.INFO
        assert "Started reloader process" in caplog.records[-1].message
        
        reloader.shutdown()
        assert caplog.records[-2].levelno == logging.INFO
        assert "Shutdown reloader process" in caplog.records[-2].message

@pytest.mark.parametrize("reloader_class", [WatchGodReload])
def test_reloader_should_not_startup_without_reload(touch_soon, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    config = Config(app="tests.test_config:asgi_app", reload=False)
    
    with as_cwd(tmp_path):
        reloader = self._setup_reloader(config)
        assert not config.should_reload
        with pytest.raises(Exception, match="Reloader should not start without reload enabled"):
            reloader.startup()

@pytest.mark.parametrize("reloader_class", [WatchGodReload])
def test_reloader_should_detect_multiple_changes(touch_soon, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    app_dir = tmp_path / "app"
    app_file = app_dir / "file.py"
    app_dir.mkdir()
    app_file.touch()

    with as_cwd(tmp_path):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["app*"])
        reloader = self._setup_reloader(config)
        assert self._reload_tester(touch_soon, reloader, app_file)

        # Simulate multiple file changes
        for i in range(3):
            (app_dir / f"file_{i}.py").touch()
        
        assert self._reload_tester(touch_soon, reloader, *[app_dir / f"file_{i}.py" for i in range(3)])
        assert caplog.records[-1].levelno == logging.INFO
        assert "WatchGodReload detected changes" in caplog.records[-1].message

        reloader.shutdown()