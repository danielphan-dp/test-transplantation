import os
import pytest

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.mark.parametrize('protocol', [3, 4])
def test_reset_environment_variable(app, protocol):
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

@pytest.mark.parametrize('protocol', [3, 4])
def test_reset_environment_variable_not_set(app, protocol):
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

@pytest.mark.parametrize('protocol', [3, 4])
def test_pickle_app_with_static_after_reset(app, protocol):
    app.route("/")(handler)
    app.after_server_start(stop)
    app.static("/static", "/tmp/static")
    app.router.reset()
    app.signal_router.reset()
    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    assert up_p_app
    up_p_app.run(single_process=True)