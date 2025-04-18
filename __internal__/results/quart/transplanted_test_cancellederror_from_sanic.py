# Transplanted from tests/test_cancellederror.py to test src/quart/asgi.py

import asyncio
import pytest
from quart import Quart, jsonify
from quart.asgi import ASGIHTTPConnection
from hypercorn.typing import HTTPScope, ASGIReceiveCallable, ASGISendCallable

@pytest.fixture
def app():
    app = Quart(__name__)

    @app.route('/')
    async def handler():
        raise asyncio.CancelledError("STOP!!")

    @app.errorhandler(asyncio.CancelledError)
    async def handle_cancel(error):
        return jsonify({"message": str(error)}), 418

    return app

@pytest.mark.asyncio
async def test_can_raise_in_handler(app):
    test_client = app.test_client()
    response = await test_client.get('/')
    assert response.status_code == 418
    assert (await response.get_json())["message"] == "STOP!!"

@pytest.mark.asyncio
async def test_asgi_http_connection_cancelled_error(app):
    scope = HTTPScope(
        type="http",
        asgi={"version": "3.0", "spec_version": "2.1"},
        method="GET",
        scheme="http",
        path="/",
        query_string=b"",
        headers=[],
        client=("127.0.0.1", 12345),
        server=("127.0.0.1", 8000),
        extensions={},
        http_version="1.1",
    )

    async def mock_receive() -> ASGIReceiveCallable:
        return {"type": "http.request"}

    async def mock_send(message: ASGISendCallable) -> None:
        assert message["type"] == "http.response.start"
        assert message["status"] == 418

    connection = ASGIHTTPConnection(app, scope)
    await connection(mock_receive, mock_send)