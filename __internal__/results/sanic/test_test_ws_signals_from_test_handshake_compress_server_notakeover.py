import base64
import secrets
from typing import Any, Callable, Coroutine
import pytest
from websockets.client import WebSocketClientProtocol
from sanic import Request, Sanic, Websocket

MimicClientType = Callable[[WebSocketClientProtocol], Coroutine[None, None, Any]]

@pytest.fixture
def simple_ws_mimic_client():
    async def client_mimic(ws: WebSocketClientProtocol):
        await ws.send("test 1")
        await ws.recv()
        await ws.send("test 2")
        await ws.recv()
    return client_mimic

def signalapp(app):
    @app.signal("websocket.handler.before")
    async def ws_before(request: Request, websocket: Websocket):
        app.ctx.seq.append("before")
        await websocket.send("before: " + await websocket.recv())

    @app.signal("websocket.handler.after")
    async def ws_after(request: Request, websocket: Websocket):
        app.ctx.seq.append("after")
        await websocket.send("after: " + await websocket.recv())

    @app.signal("websocket.handler.exception")
    async def ws_exception(request: Request, websocket: Websocket, exception: Exception):
        app.ctx.seq.append("exception")
        await websocket.send(f"exception: {exception}")

    @app.websocket("/ws")
    async def ws_handler(request: Request, ws: Websocket):
        app.ctx.seq.append("ws")

    @app.websocket("/wserror")
    async def ws_error(request: Request, ws: Websocket):
        app.ctx.seq.append("wserror")
        raise Exception(await ws.recv())

def test_ws_signals_with_exception_handling(app: Sanic, simple_ws_mimic_client: MimicClientType):
    signalapp(app)
    app.ctx.seq = []
    _, ws_proxy = app.test_client.websocket("/wserror", mimic=simple_ws_mimic_client)
    assert ws_proxy.client_received == ["exception: test error"]
    assert app.ctx.seq == ["wserror", "exception"]

def test_ws_signals_with_multiple_clients(app: Sanic, simple_ws_mimic_client: MimicClientType):
    signalapp(app)
    app.ctx.seq = []
    _, ws_proxy1 = app.test_client.websocket("/ws", mimic=simple_ws_mimic_client)
    _, ws_proxy2 = app.test_client.websocket("/ws", mimic=simple_ws_mimic_client)
    assert ws_proxy1.client_received == ["before: test 1", "after: test 2"]
    assert ws_proxy2.client_received == ["before: test 1", "after: test 2"]
    assert app.ctx.seq == ["before", "ws", "after", "before", "ws", "after"]

def test_ws_signals_order_of_operations(app: Sanic, simple_ws_mimic_client: MimicClientType):
    signalapp(app)
    app.ctx.seq = []
    _, ws_proxy = app.test_client.websocket("/ws", mimic=simple_ws_mimic_client)
    assert app.ctx.seq == ["before", "ws", "after"]