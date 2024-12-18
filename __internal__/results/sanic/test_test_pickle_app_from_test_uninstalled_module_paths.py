import os
import pytest
from sanic import Sanic

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.mark.parametrize('protocol', [3, 4])
def test_pickle_app_with_reset(app, protocol):
    app.route("/")(lambda request: "Hello, World!")
    app.after_server_start(lambda s, r: None)
    app.router.reset()
    app.signal_router.reset()
    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    assert up_p_app
    up_p_app.run(single_process=True, port=8000)

def test_reset_environment_variable():
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_reset_without_environment_variable():
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ