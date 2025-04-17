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
    assert isinstance(app, web.Application)

def test_app_response_prepare_signal(app) -> None:
    assert app.on_response_prepare is not None

def test_app_call_multiple_times(app) -> None:
    assert app is app()

def test_app_response_prepare_freeze(app) -> None:
    assert not app.on_response_prepare.is_frozen()

def test_app_mocked_methods(app) -> None:
    app.some_method = mock.Mock(return_value='mocked')
    assert app.some_method() == 'mocked'