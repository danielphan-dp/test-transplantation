import pytest
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.statreload import StatReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from pathlib import Path
from tests.utils import as_cwd

@pytest.mark.parametrize("reloader_class, expected_should_reload", [
    (StatReload, True),
    (WatchFilesReload, True),
])
def test_reloader_initialization_should_reload(reloader_class, expected_should_reload):
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = _setup_reloader(config)

    assert config.should_reload == expected_should_reload
    reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload])
def test_reload_when_python_file_is_changed_with_invalid_file(touch_soon):
    invalid_file = Path("invalid_path/main.py")

    with as_cwd(Path(".")):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = _setup_reloader(config)

        with pytest.raises(FileNotFoundError):
            touch_soon(invalid_file)
            reloader.restart()

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class", [StatReload, WatchFilesReload])
def test_reloader_should_not_start_if_not_configured():
    config = Config(app="tests.test_config:asgi_app", reload=False)
    reloader = _setup_reloader(config)

    assert not config.should_reload
    reloader.shutdown()