import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.parametrize('reloader_class', [pytest.param(WatchFilesReload)])
def test_reload_tester_edge_cases(touch_soon, reloader_class):
    reload_path = Path("path/to/reload")
    empty_file = reload_path / "empty_file.txt"
    non_existent_file = reload_path / "non_existent_file.txt"
    
    with as_cwd(reload_path):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=[".*", "*.txt"],
            reload_excludes=["*.py"],
        )
        reloader = _setup_reloader(config)

        # Test with an empty file
        empty_file.touch()
        assert self._reload_tester(touch_soon, reloader, empty_file)

        # Test with a non-existent file
        assert self._reload_tester(touch_soon, reloader, non_existent_file) is None

        reloader.shutdown()