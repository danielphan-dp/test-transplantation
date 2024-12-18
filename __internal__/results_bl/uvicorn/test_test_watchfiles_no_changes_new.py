import pytest
from uvicorn.config import Config
from uvicorn.supervisors.watchfilesreload import WatchFilesReload
from tests.utils.as_cwd import as_cwd

@pytest.mark.skipif(WatchFilesReload is None, reason='watchfiles not available')
@pytest.mark.parametrize('reloader_class', [WatchFilesReload])
def test_should_restart_edge_cases(self, reloader_class) -> None:
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = self._setup_reloader(config)

    assert isinstance(reloader, reloader_class)

    # Test first call
    assert reloader.should_restart() is None

    # Test second call
    assert reloader.should_restart() == [tmp_path / 'foobar.py']

    # Test third call raises StopIteration
    with pytest.raises(StopIteration):
        reloader.should_restart()

    reloader.shutdown()