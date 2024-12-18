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
        reloader.shutdown()
        assert caplog.records[-1].levelno == logging.WARNING
        assert "Reloading is disabled" in caplog.records[-1].message

@pytest.mark.parametrize("reloader_class", [WatchGodReload])
def test_reloader_should_handle_invalid_config(touch_soon, caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["invalid*"])
    
    with as_cwd(tmp_path):
        reloader = self._setup_reloader(config)
        assert config.should_reload
        reloader.startup()
        assert caplog.records[-1].levelno == logging.WARNING
        assert "No files to watch" in caplog.records[-1].message
        
        reloader.shutdown()