import pytest
from unittest.mock import Mock
from pathlib import Path
from time import sleep
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason="watchfiles not available")
@pytest.mark.parametrize("reloader_class", [pytest.param(WatchFilesReload)])
def test_reload_tester_edge_cases(touch_soon) -> None:
    dotted_file = Path("test_dir/.dotted")
    non_dotted_file = Path("test_dir/ext/ext.jpg")
    python_file = Path("test_dir/main.py")
    invalid_file = Path("test_dir/invalid.txt")

    dotted_file.touch()
    non_dotted_file.touch()
    python_file.touch()

    with as_cwd("test_dir"):
        config = Config(
            app="tests.test_config:asgi_app",
            reload=True,
            reload_includes=[".dotted", "ext/ext.jpg"],
        )
        reloader = WatchFilesReload(config, Mock(), [])

        assert self._reload_tester(touch_soon, reloader, dotted_file) is not None
        assert self._reload_tester(touch_soon, reloader, non_dotted_file) is not None
        assert self._reload_tester(touch_soon, reloader, python_file) is not None

        # Test with an invalid file
        with pytest.raises(AssertionError):
            self._reload_tester(touch_soon, reloader, invalid_file)

        reloader.shutdown()