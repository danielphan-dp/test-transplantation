import asyncio
import logging
from collections import Counter
import pytest
from sanic import Sanic
from conftest import get_port

@pytest.mark.asyncio
async def test_get_port_validity(caplog):
    with caplog.at_level(logging.WARNING):
        port = get_port()
        assert isinstance(port, int)
        assert 0 < port < 65536

@pytest.mark.asyncio
async def test_get_port_multiple_calls(caplog):
    with caplog.at_level(logging.WARNING):
        ports = [get_port() for _ in range(10)]
        assert len(set(ports)) == len(ports)  # Ensure all ports are unique

@pytest.mark.asyncio
async def test_get_port_zero_port(caplog):
    with caplog.at_level(logging.WARNING):
        port = get_port()
        assert port != 0  # Ensure the port is not zero

@pytest.mark.asyncio
async def test_get_port_with_uvloop(caplog):
    app = Sanic("test-uvloop")
    app.config.USE_UVLOOP = True
    with caplog.at_level(logging.WARNING):
        srv_coro = app.create_server(
            return_asyncio_server=True,
            asyncio_server_kwargs=dict(start_serving=False),
            port=get_port(),
        )
        srv = await srv_coro
        await srv.startup()
        assert srv.port == get_port()  # Ensure the server is using the correct port