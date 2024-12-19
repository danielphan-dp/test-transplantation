import pytest
from sanic import Sanic

@pytest.mark.skipif(sys.version_info < (3, 8) and (not UVLOOP_INSTALLED), reason='In 3.7 w/o uvloop the port is not always released')
def test_app_stop_functionality(app: Sanic):
    @app.after_server_start
    def after_start(*_):
        app.stop()

    app.prepare(
        version=1,
        ssl={
            "cert": localhost_dir / "fullchain.pem",
            "key": localhost_dir / "privkey.pem",
        },
    )
    
    assert app.is_running  # Ensure the app is running before stopping
    app.stop()
    assert not app.is_running  # Ensure the app is stopped

def test_app_stop_when_not_running(app: Sanic):
    with pytest.raises(RuntimeError, match="Application is not running"):
        app.stop()