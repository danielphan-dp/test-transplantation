import asyncio
from unittest import mock
import pytest
from aiohttp import web

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    ret: web.Application = mock.create_autospec(web.Application, spec_set=True)
    ret.on_response_prepare = mock.Mock()
    ret.on_response_prepare.freeze()
    return ret

def test_app_instance(app) -> None:
    assert app is app()

def test_app_response_prepare_signal(app) -> None:
    assert hasattr(app, 'on_response_prepare')
    assert callable(app.on_response_prepare)

def test_app_response_prepare_freeze(app) -> None:
    assert not app.on_response_prepare.is_frozen()

def test_app_multiple_calls(app) -> None:
    app_instance_1 = app()
    app_instance_2 = app()
    assert app_instance_1 is app_instance_2

def test_app_mocked_methods(app) -> None:
    app.some_method = mock.Mock(return_value='mocked')
    result = app.some_method()
    app.some_method.assert_called_once()
    assert result == 'mocked'