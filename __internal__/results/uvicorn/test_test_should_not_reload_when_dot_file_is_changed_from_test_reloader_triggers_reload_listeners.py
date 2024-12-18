import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchgodreload import WatchGodReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_initialize_with_different_classes(reloader_class, touch_soon) -> None:
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = _setup_reloader(config)

    assert config.should_reload
    reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reload_when_non_python_file_is_changed(reloader_class, touch_soon) -> None:
    file = Path("non_python_file.txt")
    file.touch()

    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        assert not _reload_tester(touch_soon, reloader, file)

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchGodReload, WatchFilesReload])
def test_reloader_should_not_trigger_on_unchanged_file(reloader_class, touch_soon) -> None:
    file = Path("unchanged_file.py")
    file.touch()

    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        assert not _reload_tester(touch_soon, reloader, file)

        reloader.shutdown()