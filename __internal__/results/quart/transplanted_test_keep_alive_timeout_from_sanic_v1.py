# This test file was generated from tests/test_keep_alive_timeout.py to test src/quart/app.py through test transplantation.

import asyncio
import pytest
from quart import Quart, websocket
from quart.testing import QuartClient

# Configuration for testing keep-alive timeout
CONFIG_FOR_TESTS = {"KEEP_ALIVE_TIMEOUT": 2, "KEEP_ALIVE": True}

# Initialize Quart app instances for different test scenarios
keep_alive_timeout_app_reuse = Quart(__name__)
keep_alive_app_client_timeout = Quart(__name__)
keep_alive_app_server_timeout = Quart(__name__)
keep_alive_app_context = Quart(__name__)

# Update app configurations
keep_alive_timeout_app_reuse.config.update(CONFIG_FOR_TESTS)
keep_alive_app_client_timeout.config.update(CONFIG_FOR_TESTS)
keep_alive_app_server_timeout.config.update(CONFIG_FOR_TESTS)
keep_alive_app_context.config.update(CONFIG_FOR_TESTS)

# Define routes for the apps
@keep_alive_timeout_app_reuse.route("/1")
async def handler1():
    return "OK"

@keep_alive_app_client_timeout.route("/1")
async def handler2():
    return "OK"

@keep_alive_app_server_timeout.route("/1")
async def handler3():
    return "OK"

@keep_alive_app_context.route("/ctx", methods=["POST"])
async def set_ctx():
    websocket._get_current_object().ctx.foo = "hello"
    return "OK"

@keep_alive_app_context.route("/ctx", methods=["GET"])
async def get_ctx():
    return websocket._get_current_object().ctx.foo

@pytest.mark.asyncio
async def test_keep_alive_timeout_reuse():
    """Test that the server and client successfully reuse the connection when both have longer keep-alive timeouts."""
    client = QuartClient(keep_alive_timeout_app_reuse)
    async with client:
        headers = {"Connection": "keep-alive"}
        response = await client.get("/1", headers=headers)
        assert response.status_code == 200
        assert await response.get_data(as_text=True) == "OK"

        await asyncio.sleep(1)

        response = await client.get("/1")
        assert response.status_code == 200
        assert await response.get_data(as_text=True) == "OK"

@pytest.mark.asyncio
async def test_keep_alive_client_timeout():
    """Test that the client creates a new connection when its keep-alive timeout is shorter than the server's."""
    client = QuartClient(keep_alive_app_client_timeout)
    async with client:
        headers = {"Connection": "keep-alive"}
        response = await client.get("/1", headers=headers)
        assert response.status_code == 200
        assert await response.get_data(as_text=True) == "OK"

        await asyncio.sleep(2)

        response = await client.get("/1")
        assert response.status_code == 200
        assert await response.get_data(as_text=True) == "OK"

@pytest.mark.asyncio
async def test_keep_alive_server_timeout():
    """Test that the client handles server connection reset when the server's keep-alive timeout is shorter."""
    client = QuartClient(keep_alive_app_server_timeout)
    async with client:
        headers = {"Connection": "keep-alive"}
        response = await client.get("/1", headers=headers)
        assert response.status_code == 200
        assert await response.get_data(as_text=True) == "OK"

        await asyncio.sleep(3)

        response = await client.get("/1")
        assert response.status_code == 200
        assert await response.get_data(as_text=True) == "OK"

@pytest.mark.asyncio
async def test_keep_alive_connection_context():
    """Test that the connection context is maintained across requests."""
    client = QuartClient(keep_alive_app_context)
    async with client:
        headers = {"Connection": "keep-alive"}
        response = await client.post("/ctx", headers=headers)
        assert response.status_code == 200

        await asyncio.sleep(1)

        response = await client.get("/ctx")
        assert response.status_code == 200
        assert await response.get_data(as_text=True) == "hello"