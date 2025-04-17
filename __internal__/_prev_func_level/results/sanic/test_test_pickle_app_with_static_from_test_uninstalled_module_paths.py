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
def test_pickle_app_with_static_and_reset(app, protocol):
    app.route("/")(handler)
    app.after_server_start(stop)
    app.static("/static", "/tmp/static")
    app.router.reset()
    app.signal_router.reset()
    
    # Ensure the environment variable is reset before pickling
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

    p_app = pickle.dumps(app, protocol=protocol)
    del app
    up_p_app = pickle.loads(p_app)
    
    assert up_p_app
    up_p_app.run(single_process=True)

def handler(request):
    return "Hello, World!"

def stop(app, loop):
    pass