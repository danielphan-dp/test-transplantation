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
    app.route("/")(handler)
    app.after_server_start(stop)
    app.router.reset()
    app.signal_router.reset()
    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    assert up_p_app
    up_p_app.run(single_process=True, port=port)

def test_pickle_app_no_environment_variable(app, protocol):
    assert 'SANIC_MOTD_OUTPUT' not in os.environ
    app.route("/")(handler)
    app.after_server_start(stop)
    app.router.reset()
    app.signal_router.reset()
    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    assert up_p_app
    up_p_app.run(single_process=True, port=port)

def test_pickle_app_with_missing_app(app, protocol):
    del app
    with pytest.raises(NameError):
        pickle.dumps(app, protocol=protocol)