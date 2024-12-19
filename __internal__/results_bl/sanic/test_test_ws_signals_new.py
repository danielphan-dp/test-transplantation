import pytest
from sanic import Sanic
from sanic.websocket import Websocket
from sanic.request import Request

def test_ws_exception_signal(app: Sanic, simple_ws_mimic_client):
    signalapp(app)

    app.ctx.seq = []
    _, ws_proxy = app.test_client.websocket("/wserror", mimic=simple_ws_mimic_client)
    ws_proxy.send("trigger exception")
    
    assert ws_proxy.client_received == ["exception: trigger exception"]
    assert app.ctx.seq == ["wserror", "exception"]

def test_ws_before_signal(app: Sanic, simple_ws_mimic_client):
    signalapp(app)

    app.ctx.seq = []
    _, ws_proxy = app.test_client.websocket("/ws", mimic=simple_ws_mimic_client)
    ws_proxy.send("test 1")
    
    assert ws_proxy.client_received == ["before: test 1"]
    assert app.ctx.seq == ["before", "ws"]

def test_ws_after_signal(app: Sanic, simple_ws_mimic_client):
    signalapp(app)

    app.ctx.seq = []
    _, ws_proxy = app.test_client.websocket("/ws", mimic=simple_ws_mimic_client)
    ws_proxy.send("test 2")
    
    assert ws_proxy.client_received == ["before: test 1", "after: test 2"]
    assert app.ctx.seq == ["before", "ws", "after"]