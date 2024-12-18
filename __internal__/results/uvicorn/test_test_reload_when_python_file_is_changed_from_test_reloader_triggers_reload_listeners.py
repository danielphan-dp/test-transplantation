import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_initialize_with_different_classes(reloader_class) -> None:
    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)
        assert reloader is not None
        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_does_not_start_when_reload_is_false(reloader_class) -> None:
    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=False)
        reloader = _setup_reloader(config)
        assert not config.should_reload
        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_initialization_with_invalid_config(reloader_class) -> None:
    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        config.reload_delay = -1  # Invalid delay
        with pytest.raises(ValueError):
            _setup_reloader(config)

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_trigger_on_file_change(touch_soon, reloader_class) -> None:
    file = Path("main.py")
    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        changes = _reload_tester(touch_soon, reloader, file)
        assert changes == [file]

        reloader.shutdown()