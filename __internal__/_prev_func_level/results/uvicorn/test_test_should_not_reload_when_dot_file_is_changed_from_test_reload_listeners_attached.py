import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
def test_reloader_should_initialize_with_different_classes(reloader_class, touch_soon) -> None:
    file = Path("test_file.py")
    
    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        assert config.should_reload
        reloader.startup()
        
        # Simulate file change
        touch_soon(file)
        assert self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()

def test_reloader_should_not_reload_when_non_python_file_is_changed(touch_soon) -> None:
    file = Path("test_file.txt")

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()