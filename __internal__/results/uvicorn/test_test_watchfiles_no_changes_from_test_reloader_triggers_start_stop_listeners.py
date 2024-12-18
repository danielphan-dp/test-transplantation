import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils import as_cwd

@pytest.mark.parametrize("reloader_class", [WatchFilesReload, WatchGodReload])
def test_reloader_initialization_with_different_classes(reloader_class) -> None:
    sub_dir = Path("app/sub")

    with as_cwd(Path("reload_path")):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_excludes=[str(sub_dir)],
        )
        reloader = _setup_reloader(config)

        assert isinstance(reloader, reloader_class)
        assert config.should_reload

        reloader.shutdown()

def test_reloader_should_not_start_if_not_configured() -> None:
    config = Config(app="tests.test_config:asgi_app", reload=False)

    with pytest.raises(Exception, match="Reloader not configured"):
        _setup_reloader(config)

def test_reloader_should_restart_on_file_change(touch_soon) -> None:
    file = Path("main.py")
    config = Config(app="tests.test_config:asgi_app", reload=True)

    with as_cwd(Path("reload_path")):
        reloader = _setup_reloader(config)
        reloader.restart()

        touch_soon(file)
        assert reloader.should_restart() is not None

        reloader.shutdown()