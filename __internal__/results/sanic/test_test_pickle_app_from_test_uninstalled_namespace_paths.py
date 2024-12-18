import os
import pytest

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.mark.parametrize('protocol', [3, 4])
def test_pickle_app_with_reset(app, protocol):
    app.route("/")(handler)
    app.after_server_start(stop)
    app.router.reset()
    app.signal_router.reset()
    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    assert up_p_app
    up_p_app.run(single_process=True, port=8000)

def test_pickle_app_environment_variable(app, protocol):
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    app.route("/")(handler)
    app.after_server_start(stop)
    app.router.reset()
    app.signal_router.reset()
    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    assert up_p_app
    assert os.environ['SANIC_MOTD_OUTPUT'] == 'test_value'
    up_p_app.run(single_process=True, port=8001)

def test_pickle_app_no_environment_variable(app, protocol):
    if 'SANIC_MOTD_OUTPUT' in os.environ:
        del os.environ['SANIC_MOTD_OUTPUT']
    app.route("/")(handler)
    app.after_server_start(stop)
    app.router.reset()
    app.signal_router.reset()
    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    assert up_p_app
    up_p_app.run(single_process=True, port=8002)