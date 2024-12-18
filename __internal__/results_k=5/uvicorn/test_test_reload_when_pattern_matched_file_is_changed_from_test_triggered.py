import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class, result", [(BaseReload, False), (WatchFilesReload, True)])
def test_reload_with_no_file_changes(reloader_class, result, touch_soon) -> None:
    file = Path("dummy_file.js")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = reloader_class(config)

        assert self._reload_tester(touch_soon, reloader, file) is None

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class, result", [(BaseReload, False), (WatchFilesReload, True)])
def test_reload_with_multiple_files(reloader_class, result, touch_soon) -> None:
    files = [Path(f"file_{i}.js") for i in range(3)]
    for file in files:
        file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = reloader_class(config)

        assert bool(self._reload_tester(touch_soon, reloader, *files)) == result

        reloader.shutdown()

@pytest.mark.parametrize("reloader_class, result", [(BaseReload, False), (WatchFilesReload, True)])
def test_reload_with_nonexistent_file(reloader_class, result, touch_soon) -> None:
    nonexistent_file = Path("nonexistent_file.js")

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = reloader_class(config)

        assert self._reload_tester(touch_soon, reloader, nonexistent_file) is None

        reloader.shutdown()