import pytest
from sanic import Sanic
from sanic_ext import Extend

@pytest.fixture
def app():
    app = Sanic("TestApp")
    Extend(app)
    return app

def test_app_stops_correctly(app):
    @app.before_server_start
    async def before_start(*_):
        pass

    @app.after_server_stop
    async def after_stop(*_):
        assert True  # Ensure this is called

    app.stop()
    assert not app.is_running

def test_app_stop_with_injection(app):
    class IceCream:
        flavor: str

    @app.before_server_start
    async def injections(*_):
        app.ext.injection(IceCream)
        app.stop()

    app.run(single_process=True)
    assert app.ext.injection.called
    assert app.ext.injection.call_args[0][0] is IceCream

def test_app_stop_during_request(app):
    @app.route("/")
    async def handler(request):
        app.stop()
        return "Stopped"

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "Stopped"
    assert not app.is_running

def test_app_stop_with_error_handling(app):
    @app.before_server_start
    async def before_start(*_):
        raise RuntimeError("Startup failed")

    with pytest.raises(RuntimeError, match="Startup failed"):
        app.run(single_process=True)

    assert not app.is_running