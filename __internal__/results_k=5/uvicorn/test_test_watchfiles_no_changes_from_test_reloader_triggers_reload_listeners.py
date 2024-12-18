import pytest
from pathlib import Path
from uvicorn.config import Config
from uvicorn.supervisors.basereload import BaseReload

@pytest.mark.parametrize('step, expected', [
    (1, None),
    (2, [Path('foobar.py')]),
])
def test_should_restart(step, expected):
    calls = []
    reloader = BaseReload(Config(app="tests.test_config:asgi_app", reload=True))

    def mock_should_restart():
        nonlocal step
        step += 1
        if step == 1:
            return None
        elif step == 2:
            return [Path('foobar.py')]
        else:
            raise StopIteration()

    reloader.should_restart = mock_should_restart

    if step == 1:
        assert reloader.should_restart() is None
    elif step == 2:
        assert reloader.should_restart() == [Path('foobar.py')]
    
    if step > 2:
        with pytest.raises(StopIteration):
            reloader.should_restart()