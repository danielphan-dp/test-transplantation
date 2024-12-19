import sys
import pytest
from sanic import Sanic
from sanic_ext import Extension

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.fixture
def mock_sanic_ext():
    return Extension()

@pytest.fixture
def ext_instance(mock_sanic_ext):
    return mock_sanic_ext

@pytest.mark.asyncio
async def test_stop_app_functionality(app, mock_sanic_ext, ext_instance):
    app.ext = ext_instance
    app.run(single_process=True)

    assert app.is_running is True
    app.stop()
    assert app.is_running is False

@pytest.mark.asyncio
async def test_stop_app_multiple_calls(app, mock_sanic_ext, ext_instance):
    app.ext = ext_instance
    app.run(single_process=True)

    app.stop()
    assert app.is_running is False

    app.stop()  # Calling stop again
    assert app.is_running is False

@pytest.mark.asyncio
async def test_stop_app_with_injections(app, mock_sanic_ext, ext_instance):
    class IceCream:
        flavor: str

    @app.before_server_start
    async def injections(*_):
        app.ext.injection(IceCream)

    app.run(single_process=True)
    ext_instance.injection.assert_called_with(IceCream)

    app.stop()
    assert app.is_running is False

@pytest.mark.asyncio
async def test_stop_app_without_running(app, mock_sanic_ext, ext_instance):
    app.ext = ext_instance
    app.stop()  # Stop without running
    assert app.is_running is False

@pytest.mark.asyncio
async def test_stop_app_with_error_handling(app, mock_sanic_ext, ext_instance):
    app.ext = ext_instance

    @app.before_server_start
    async def raise_error(*_):
        raise Exception("Error during start")

    with pytest.raises(Exception, match="Error during start"):
        app.run(single_process=True)

    app.stop()
    assert app.is_running is False