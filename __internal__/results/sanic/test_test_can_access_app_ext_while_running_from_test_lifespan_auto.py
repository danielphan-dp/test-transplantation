import pytest
from sanic import Sanic
from sanic_ext import Extend

@pytest.fixture
def app():
    app = Sanic("TestApp")
    Extend(app)
    return app

def test_app_stops_correctly(app):
    class IceCream:
        flavor: str

    @app.before_server_start
    async def injections(*_):
        app.ext.injection(IceCream)

    app.stop()
    with pytest.raises(RuntimeError):
        app.run(single_process=True)

def test_app_stop_during_request(app):
    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    @app.before_server_start
    async def before_start(*_):
        app.stop()

    app.run(single_process=True)
    response = app.test_client.get("/")
    assert response.status == 500

def test_app_stop_with_injection(app):
    class IceCream:
        flavor: str

    @app.before_server_start
    async def injections(*_):
        app.ext.injection(IceCream)

    app.run(single_process=True)
    app.stop()
    assert not app.is_running()