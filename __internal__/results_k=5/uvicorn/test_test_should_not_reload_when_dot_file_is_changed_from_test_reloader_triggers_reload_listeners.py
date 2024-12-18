import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from time import sleep

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_when_non_dot_file_is_changed(touch_soon) -> None:
    file = Path("test_file.txt")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_not_reload_when_file_is_not_touched(touch_soon) -> None:
    file = Path("untouched_file.txt")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_reload_multiple_files(touch_soon) -> None:
    file1 = Path("file1.txt")
    file2 = Path("file2.txt")
    file1.touch()
    file2.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert self._reload_tester(touch_soon, reloader, file1, file2)

        reloader.shutdown()

@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_not_reload_when_no_changes(touch_soon) -> None:
    file = Path("no_change_file.txt")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True)
        reloader = self._setup_reloader(config)

        assert not self._reload_tester(touch_soon, reloader, file)

        sleep(0.1)  # Allow time for any potential changes to be detected
        assert not self._reload_tester(touch_soon, reloader, file)

        reloader.shutdown()