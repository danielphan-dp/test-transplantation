import pytest
from sanic import Sanic, Request, Websocket
from typing import Any

@pytest.mark.parametrize('proxy', ['', 'proxy', 'servername'])
def test_recv_method(app: Sanic, simple_ws_mimic_client: Any, proxy: str) -> None:
    @app.websocket("/ws")
    async def ws_handler(request: Request, ws: Websocket):
        request.headers["forwarded"] = (
            "for=[2001:db8::1];proto=https;host=example.com;by=proxy"
        )
        await ws.recv()
        await ws.send("test 1")
        await ws.recv()
        await ws.send("test 2")
        await ws.recv()

    app.config.FORWARDED_SECRET = proxy
    app.config.SERVER_NAME = (
        "https://example.com" if proxy == "servername" else ""
    )
    _, ws_proxy = app.test_client.websocket(
        "/ws",
        mimic=simple_ws_mimic_client,
    )
    
    assert ws_proxy.client_sent == ["test 1", "test 2", ""]
    assert ws_proxy.client_received[0] == ws_proxy.client_received[1]
    
    if proxy == "servername":
        assert ws_proxy.client_received[0] == "wss://example.com/ws"
        assert ws_proxy.client_received[1] == "wss://example.com/ws"
    else:
        assert ws_proxy.client_received[0].startswith("ws://127.0.0.1")
        assert ws_proxy.client_received[1].startswith("ws://127.0.0.1")

    # Additional edge case tests
    await ws.send("test 3")
    await ws.recv()
    assert ws_proxy.client_sent == ["test 1", "test 2", "test 3", ""]
    
    await ws.send("test 4")
    await ws.recv()
    assert ws_proxy.client_sent == ["test 1", "test 2", "test 3", "test 4", ""]