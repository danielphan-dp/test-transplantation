import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

class CustomReload(BaseReload):
    def __init__(self, config):
        super().__init__(config)
        self.step = 0

    def should_restart(self):
        self.step += 1
        if self.step == 1:
            return None
        elif self.step == 2:
            return [Path('foobar.py')]
        else:
            raise StopIteration()

def test_custom_reloader_should_restart(tmp_path: Path):
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config)

    assert reloader.should_restart() is None
    assert reloader.should_restart() == [tmp_path / 'foobar.py']
    
    with pytest.raises(StopIteration):
        reloader.should_restart()

def test_custom_reloader_multiple_calls(tmp_path: Path):
    config = Config(app="tests.test_config:asgi_app", reload=True)
    reloader = CustomReload(config)

    assert reloader.should_restart() is None
    assert reloader.should_restart() == [tmp_path / 'foobar.py']
    
    reloader.should_restart()  # Call to advance step
    with pytest.raises(StopIteration):
        reloader.should_restart()