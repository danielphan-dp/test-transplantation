import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize("reloader_class, expected_result", [
    (WatchFilesReload, True),
    (BaseReload, False)
])
def test_reload_tester_with_file_touch(reloader_class, expected_result, touch_soon) -> None:
    file = Path("test_file.js")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = reloader_class(config)

        result = self._reload_tester(touch_soon, reloader, file)
        assert bool(result) == expected_result

        reloader.shutdown()

def test_reload_tester_no_changes(touch_soon) -> None:
    file = Path("unchanged_file.js")
    file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = WatchFilesReload(config)

        result = self._reload_tester(touch_soon, reloader, file)
        assert result is None

        reloader.shutdown()

def test_reload_tester_multiple_files(touch_soon) -> None:
    files = [Path(f"file_{i}.js") for i in range(3)]
    for file in files:
        file.touch()

    with as_cwd(Path.cwd()):
        config = Config(app="tests.test_config:asgi_app", reload=True, reload_includes=["*.js"])
        reloader = WatchFilesReload(config)

        result = self._reload_tester(touch_soon, reloader, *files)
        assert len(result) == len(files)

        reloader.shutdown()