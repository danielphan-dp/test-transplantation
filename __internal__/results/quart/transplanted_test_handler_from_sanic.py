# This test file was generated by adapting tests from tests/test_handler.py
# to test the functionality in src/quart/ctx.py through test transplantation.

import pytest
from quart import Quart, websocket
from quart.ctx import RequestContext, WebsocketContext, AppContext
from quart.globals import _cv_request, _cv_websocket, _cv_app
from quart.testing import QuartClient

@pytest.fixture
def app():
    app = Quart(__name__)

    @app.route('/')
    async def index():
        return 'Hello, World!'

    @app.websocket('/ws')
    async def ws():
        await websocket.accept()
        await websocket.send('Hello, Websocket!')
        await websocket.close()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.mark.asyncio
async def test_request_context(app, client: QuartClient):
    # Test the RequestContext push and pop
    async with app.test_request_context('/'):
        assert _cv_request.get() is not None
        assert isinstance(_cv_request.get(), RequestContext)
    assert _cv_request.get() is None

@pytest.mark.asyncio
async def test_websocket_context(app, client: QuartClient):
    # Test the WebsocketContext push and pop
    async with app.test_websocket('/ws'):
        assert _cv_websocket.get() is not None
        assert isinstance(_cv_websocket.get(), WebsocketContext)
    assert _cv_websocket.get() is None

@pytest.mark.asyncio
async def test_app_context(app):
    # Test the AppContext push and pop
    async with app.app_context():
        assert _cv_app.get() is not None
        assert isinstance(_cv_app.get(), AppContext)
    assert _cv_app.get() is None

@pytest.mark.asyncio
async def test_after_this_request(app, client: QuartClient):
    # Test the after_this_request functionality
    operations = []

    @app.route('/after')
    async def after():
        @app.after_this_request
        def after_request(response):
            operations.append(2)
            return response

        operations.append(1)
        return 'After request'

    response = await client.get('/after')
    assert response.status_code == 200
    assert operations == [1, 2]

@pytest.mark.asyncio
async def test_after_this_websocket(app):
    # Test the after_this_websocket functionality
    operations = []

    @app.websocket('/after_ws')
    async def after_ws():
        @app.after_this_websocket
        def after_websocket(response=None):
            operations.append(2)
            return response

        operations.append(1)
        await websocket.accept()
        await websocket.close()

    async with app.test_websocket('/after_ws'):
        pass

    assert operations == [1, 2]